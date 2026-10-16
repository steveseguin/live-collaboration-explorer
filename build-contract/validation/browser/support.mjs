import { chromium, expect } from '@playwright/test';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = resolve(dirname(fileURLToPath(import.meta.url)), '..');

export function readConfig() {
  const input = process.env.COHOST_ACCEPTANCE_CONFIG;
  if (!input) throw new Error('BLOCKED: Set COHOST_ACCEPTANCE_CONFIG to a private, explicit local/QA configuration. No default app target exists.');
  const config = JSON.parse(readFileSync(resolve(input), 'utf8'));
  if (!['local', 'qa'].includes(config.environmentKind)) throw new Error('Only explicit local/qa targets are allowed.');
  const unresolved = JSON.stringify(config).match(/REPLACE_[A-Z_]+/);
  if (unresolved) throw new Error('BLOCKED: Replace all configuration placeholders first.');
  for (const key of ['implementationRevision', 'engineRevision']) {
    if (!/^[a-f\d]{7,64}$/i.test(config[key] ?? '')) throw new Error(`Missing pinned ${key}`);
  }
  for (const key of ['hostConsoleUrl', 'otherEventConsoleUrl']) assertAllowed(config[key], config);
  if (!config.expectedEventId || !config.otherEventId || config.expectedEventId === config.otherEventId) throw new Error('Configure two distinct prepared event IDs.');
  for (const key of ['hostVideo', 'hostAudio', 'guestVideo', 'guestAudio']) {
    config[key] = resolve(here, config[key]);
    if (!existsSync(config[key])) throw new Error(`BLOCKED: Generate controlled media fixture ${key}.`);
  }
  if (config.hostAuthState) config.hostAuthState = resolve(here, config.hostAuthState);
  return config;
}

export function assertAllowed(url, config) {
  const target = new URL(url);
  if (!config.allowedOrigins?.includes(target.origin)) throw new Error('Target origin is not explicitly allowlisted in private configuration.');
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(target.hostname);
  // Reserved .test hosts support isolated QA labs; review any deployment-specific extension.
  const qa = target.hostname.endsWith('.test');
  if (!local && !qa) throw new Error('This harness refuses non-local/non-QA targets; no production action is authorized.');
  if (target.protocol !== 'https:' && !local) throw new Error('Non-local targets require HTTPS.');
}

async function actor(config, kind, storageState) {
  const browser = await chromium.launch({
    channel: config.channel || undefined,
    headless: config.headless !== false,
    args: [
      '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
      `--use-file-for-fake-video-capture=${config[`${kind}Video`]}`,
      `--use-file-for-fake-audio-capture=${config[`${kind}Audio`]}`,
    ],
  });
  const context = await browser.newContext({
    storageState: storageState || undefined,
    ignoreHTTPSErrors: config.ignoreHTTPSErrors === true,
    viewport: { width: 1280, height: 720 }, locale: 'en-US',
  });
  for (const origin of new Set([...config.allowedOrigins, ...config.engineOrigins])) {
    await context.grantPermissions(['camera', 'microphone'], { origin });
  }
  await context.tracing.start({ screenshots: true, snapshots: true });
  return { browser, context };
}

export async function createLab(config) {
  const host = await actor(config, 'host', config.hostAuthState);
  let guest;
  try { guest = await actor(config, 'guest'); }
  catch (error) { await host.browser.close(); throw error; }
  const consolePage = await host.context.newPage();
  return { config, host, guest, consolePage, studio: null, guestPage: null };
}

export async function launchStudio(lab) {
  await lab.consolePage.goto(lab.config.hostConsoleUrl);
  const popup = lab.consolePage.waitForEvent('popup');
  await lab.consolePage.getByRole('button', { name: 'Open co-host studio', exact: true }).click();
  lab.studio = await popup;
  await lab.studio.waitForURL(url => lab.config.allowedOrigins.includes(url.origin));
  assertAllowed(lab.studio.url(), lab.config);
  await expect(lab.studio.getByRole('region', { name: 'Co-host studio', exact: true })).toBeVisible();
  await expect(lab.consolePage.getByRole('region', { name: 'Listing management', exact: true })).toBeVisible();
  await expect(lab.consolePage.getByRole('region', { name: 'Public buyer chat', exact: true })).toBeVisible();
  return lab.studio;
}

export async function prepareAndInvite(lab) {
  await launchStudio(lab);
  await lab.studio.getByRole('button', { name: 'Prepare host', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Host readiness', exact: true })).toHaveText('Ready');
  await lab.studio.getByRole('button', { name: 'Create guest invite', exact: true }).click();
  const link = await lab.studio.getByRole('textbox', { name: 'Guest invitation link', exact: true }).inputValue();
  assertAllowed(link, lab.config);
  lab.guestPage = await lab.guest.context.newPage();
  await lab.guestPage.goto(link);
  await expect(lab.guestPage.getByRole('region', { name: 'Join as guest', exact: true })).toBeVisible();
  return link;
}

export async function joinBackstage(lab) {
  await prepareAndInvite(lab);
  await lab.guestPage.getByRole('button', { name: 'Check devices', exact: true }).click();
  await expect(lab.guestPage.getByRole('status', { name: 'Device readiness', exact: true })).toHaveText('Ready');
  await lab.guestPage.getByRole('button', { name: 'Join backstage', exact: true }).click();
  await expect(lab.guestPage.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Backstage');
  await expect(lab.studio.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Backstage');
}

export async function diagnostics(page) {
  const data = await page.evaluate(() => {
    if (!window.__COHOST_DIAGNOSTICS__?.snapshot) return null;
    return window.__COHOST_DIAGNOSTICS__.snapshot();
  });
  expect(data, 'Missing read-only test-environment diagnostic API').not.toBeNull();
  expect(data.schemaVersion).toBe(1);
  for (const key of ['eventId', 'eventState', 'publishingState', 'contributionTransportState']) {
    expect(typeof data[key], `Missing diagnostic string ${key}`).toBe('string');
    expect(data[key].length, `Empty diagnostic string ${key}`).toBeGreaterThan(0);
  }
  for (const key of ['engineGeneration', 'programRevision', 'programPublishers',
    'activeCaptureTrackCount', 'usableVideoTracks', 'usableAudioTracks', 'rejectedMessages']) {
    expect(Number.isInteger(data[key]), `Missing diagnostic integer ${key}`).toBe(true);
    expect(data[key], `Negative diagnostic counter ${key}`).toBeGreaterThanOrEqual(0);
  }
  for (const key of ['sessionId', 'engineInstanceId', 'publisherSessionId']) {
    expect(data[key] === null || (typeof data[key] === 'string' && data[key].length > 0),
      `${key} must be a real identifier or explicit null`).toBe(true);
  }
  if (await page.getByRole('region', { name: 'Co-host studio', exact: true }).count()) {
    for (const key of ['sessionId', 'engineInstanceId']) expect(data[key]).not.toBeNull();
  }
  expect(Object.hasOwn(data, 'guest'), 'Missing guest diagnostic state').toBe(true);
  if (data.guest !== null) {
    expect(typeof data.guest.id).toBe('string');
    expect(data.guest.id.length).toBeGreaterThan(0);
    expect(Number.isInteger(data.guest.generation)).toBe(true);
    expect(data.guest.generation).toBeGreaterThanOrEqual(0);
    expect(typeof data.guest.state).toBe('string');
    expect(typeof data.guest.admitted).toBe('boolean');
  }
  return data;
}

export async function disposeLab(lab, testInfo) {
  const pages = [lab.consolePage, lab.studio, lab.guestPage].filter(Boolean);
  for (const [index, page] of pages.entries()) {
    if (!page.isClosed()) {
      const path = testInfo.outputPath(`view-${index}.png`);
      await page.screenshot({ path, fullPage: true }).catch(() => {});
      if (existsSync(path)) await testInfo.attach(`view-${index}`, { path, contentType: 'image/png' });
    }
  }
  await Promise.all([lab.host.context.tracing.stop({ path: testInfo.outputPath('host-trace.zip') }).catch(() => {}),
    lab.guest.context.tracing.stop({ path: testInfo.outputPath('guest-trace.zip') }).catch(() => {})]);
  await Promise.all([lab.host.browser.close(), lab.guest.browser.close()]);
}
