import { test as base, expect } from '@playwright/test';
import { createLab, diagnostics, disposeLab, joinBackstage, launchStudio, prepareAndInvite, readConfig } from './support.mjs';

const test = base.extend({
  lab: async ({}, use, testInfo) => {
    const lab = await createLab(readConfig());
    try { await use(lab); } finally { await disposeLab(lab, testInfo); }
  },
});

test('T001 console launch remains compact and singleton', async ({ lab }) => {
  // Denial must be exercised before an owner exists, otherwise focusing the
  // existing owner is a legitimate outcome rather than a blocked-popup error.
  const denied = await lab.host.context.newPage();
  await denied.addInitScript(() => { window.open = () => null; });
  await denied.goto(lab.config.hostConsoleUrl);
  await denied.getByRole('button', { name: 'Open co-host studio', exact: true }).click();
  await expect(denied.getByRole('alert')).toContainText(/pop.?up/i);
  expect((await diagnostics(denied)).activeCaptureTrackCount).toBe(0);
  expect((await diagnostics(denied)).programPublishers).toBe(0);
  await denied.close();
  await launchStudio(lab);
  const first = await diagnostics(lab.studio);
  await lab.consolePage.getByRole('button', { name: 'Open co-host studio', exact: true }).click();
  const second = await diagnostics(lab.studio);
  expect(second.sessionId).toBe(first.sessionId);
  expect(second.engineInstanceId).toBe(first.engineInstanceId);
  expect(lab.host.context.pages().filter(page => !page.isClosed())).toHaveLength(2);
  expect(second.programPublishers).toBeLessThanOrEqual(1);
});

test('T004 explicit checks produce backstage, not on air', async ({ lab }) => {
  await prepareAndInvite(lab);
  const initial = await diagnostics(lab.guestPage);
  expect(initial.activeCaptureTrackCount).toBe(0);
  await lab.guestPage.getByRole('button', { name: 'Check devices', exact: true }).click();
  await expect(lab.guestPage.getByRole('status', { name: 'Device readiness', exact: true })).toHaveText('Ready');
  const ready = await diagnostics(lab.guestPage);
  expect(ready.usableVideoTracks).toBeGreaterThan(0);
  expect(ready.usableAudioTracks).toBeGreaterThan(0);
  expect(ready.contributionTransportState).toBe('connected');
  await lab.guestPage.getByRole('button', { name: 'Join backstage', exact: true }).click();
  await expect(lab.guestPage.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Backstage');
  await expect(lab.studio.getByRole('button', { name: 'Bring guest on air', exact: true })).toBeDisabled();
  const host = await diagnostics(lab.studio);
  expect(host.guest.admitted).toBe(false);
  expect(host.publishingState).toBe('idle');
});

test('T007 private messages stay in the private conversation', async ({ lab }) => {
  await joinBackstage(lab);
  const hostText = `private-host-${Date.now()}`;
  const guestText = `private-guest-${Date.now()}`;
  await lab.studio.getByRole('textbox', { name: 'Private message', exact: true }).fill(hostText);
  await lab.studio.getByRole('button', { name: 'Send private message', exact: true }).click();
  await expect(lab.guestPage.getByRole('region', { name: 'Backstage conversation', exact: true })).toContainText(hostText);
  await expect(lab.guestPage.getByRole('region', { name: 'Backstage conversation', exact: true }).getByText(hostText, { exact: true })).toHaveCount(1);
  await lab.guestPage.getByRole('textbox', { name: 'Private message', exact: true }).fill(guestText);
  await lab.guestPage.getByRole('button', { name: 'Send private message', exact: true }).click();
  await expect(lab.studio.getByRole('region', { name: 'Backstage conversation', exact: true })).toContainText(guestText);
  await expect(lab.studio.getByRole('region', { name: 'Backstage conversation', exact: true }).getByText(guestText, { exact: true })).toHaveCount(1);
  const publicChat = lab.consolePage.getByRole('region', { name: 'Public buyer chat', exact: true });
  await expect(publicChat).not.toContainText(hostText);
  await expect(publicChat).not.toContainText(guestText);
});

test('T012 a second guest is rejected and replacement is explicit', async ({ lab }) => {
  const invite = await prepareAndInvite(lab);
  await lab.guestPage.getByRole('button', { name: 'Check devices', exact: true }).click();
  await expect(lab.guestPage.getByRole('status', { name: 'Device readiness', exact: true })).toHaveText('Ready');
  await lab.guestPage.getByRole('button', { name: 'Join backstage', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Backstage');
  const first = await diagnostics(lab.studio);
  const intruder = await lab.guest.browser.newContext({ viewport: { width: 360, height: 640 } });
  const other = await intruder.newPage();
  await other.goto(invite);
  await expect(other.getByRole('alert')).toContainText(/used|redeemed|full|unavailable/i);
  expect((await diagnostics(lab.studio)).guest.generation).toBe(first.guest.generation);
  await lab.studio.getByRole('button', { name: 'Remove guest', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Removed');
  await lab.studio.getByRole('button', { name: 'Create guest invite', exact: true }).click();
  const replacement = await lab.studio.getByRole('textbox', { name: 'Guest invitation link', exact: true }).inputValue();
  expect(replacement).not.toBe(invite);
  await other.goto(replacement);
  await other.getByRole('button', { name: 'Check devices', exact: true }).click();
  await expect(other.getByRole('status', { name: 'Device readiness', exact: true })).toHaveText('Ready');
  await other.getByRole('button', { name: 'Join backstage', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Backstage');
  expect((await diagnostics(lab.studio)).guest.generation).toBeGreaterThan(first.guest.generation);
  await lab.guestPage.reload();
  await expect(lab.guestPage.getByRole('alert')).toContainText(/removed|revoked|expired|unavailable/i);
  await intruder.close();
});

test('T016 publisher start and stop do not change event lifecycle', async ({ lab }) => {
  await launchStudio(lab);
  await lab.studio.getByRole('button', { name: 'Prepare host', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Host readiness', exact: true })).toHaveText('Ready');
  const before = await diagnostics(lab.studio);
  const eventMutations = [];
  lab.host.context.on('request', request => {
    if (request.method() !== 'POST') return;
    try {
      const payload = request.postDataJSON();
      for (const value of Array.isArray(payload) ? payload : [payload]) {
        if (/(?:StartEvent|EndEvent)/.test(value?.operationName ?? '')) eventMutations.push(value.operationName);
      }
    } catch { /* Non-GraphQL requests are checked by protocol/media cases. */ }
  });
  await lab.studio.getByRole('button', { name: 'Start publishing', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Publishing status', exact: true })).toHaveText('Publishing');
  await lab.studio.getByRole('button', { name: 'Stop publishing', exact: true }).click();
  await expect(lab.studio.getByRole('status', { name: 'Publishing status', exact: true })).toHaveText('Stopped');
  expect((await diagnostics(lab.studio)).eventState).toBe(before.eventState);
  expect(eventMutations).toEqual([]);
});

test('T017 console tabs and reload preserve the original studio binding', async ({ lab }) => {
  await joinBackstage(lab);
  const before = await diagnostics(lab.studio);
  await lab.consolePage.getByRole('tab', { name: 'Listings', exact: true }).click();
  await lab.consolePage.reload();
  await lab.consolePage.goto(lab.config.otherEventConsoleUrl);
  const after = await diagnostics(lab.studio);
  expect(after.eventId).toBe(lab.config.expectedEventId);
  expect(after.sessionId).toBe(before.sessionId);
  expect(after.engineInstanceId).toBe(before.engineInstanceId);
  expect(after.engineGeneration).toBe(before.engineGeneration);
  expect(after.guest.generation).toBe(before.guest.generation);
  expect(after.guest.state).toBe('backstage');
});

test('T028 forged studio messages cannot mutate the session', async ({ lab }) => {
  await joinBackstage(lab);
  const before = await diagnostics(lab.studio);
  await lab.studio.evaluate(({ eventId, sessionId, generation }) => {
    const payloads = [
      { type: 'ADMIT', schemaVersion: 999 },
      { type: 'ADMIT', schemaVersion: 1, eventId: 'wrong-event', sessionId, generation },
      { type: 'ADMIT', schemaVersion: 1, eventId, sessionId: 'wrong-session', generation },
      { type: 'ADMIT', schemaVersion: 1, eventId, sessionId, generation: generation - 1 },
      { type: 'STOP_OUTPUT', schemaVersion: 1, eventId, sessionId, sequence: -1 },
    ];
    for (const payload of payloads) window.postMessage(payload, window.location.origin);
  }, { eventId: before.eventId, sessionId: before.sessionId, generation: before.guest.generation });
  // These probes come from the studio window, not the trusted engine/service.
  // T002/T003/T029 additionally exercise authorization, races and replay there.
  await expect.poll(async () => (await diagnostics(lab.studio)).rejectedMessages)
    .toBeGreaterThanOrEqual(before.rejectedMessages + 5);
  await expect(lab.studio.getByRole('status', { name: 'Guest status', exact: true })).toHaveText('Backstage');
  const after = await diagnostics(lab.studio);
  expect(after.programRevision).toBe(before.programRevision);
  expect(after.publisherSessionId).toBe(before.publisherSessionId);
  expect(after.guest.admitted).toBe(false);
  expect(after.rejectedMessages).toBeGreaterThanOrEqual(before.rejectedMessages + 5);
});

test('T032 host and guest critical viewport layouts stay usable', async ({ lab }) => {
  await joinBackstage(lab);
  await expect(lab.consolePage.getByRole('region', { name: 'Listing management', exact: true })).toBeVisible();
  await expect(lab.consolePage.getByRole('region', { name: 'Public buyer chat', exact: true })).toBeVisible();
  await lab.guestPage.setViewportSize({ width: 360, height: 640 });
  await expect(lab.guestPage.getByRole('button', { name: 'Leave show', exact: true })).toBeInViewport();
  await expect(lab.guestPage.getByRole('textbox', { name: 'Private message', exact: true })).toBeInViewport();
  const geometry = await lab.guestPage.evaluate(() => ({
    width: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
  }));
  expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.width);
});
