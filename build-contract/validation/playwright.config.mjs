import { defineConfig } from '@playwright/test';
import { readFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const here = dirname(fileURLToPath(import.meta.url));
const output = process.env.COHOST_ACCEPTANCE_RUN
  ? resolve(process.env.COHOST_ACCEPTANCE_RUN) : resolve(here, 'runs/browser');
const relativeOutput = relative(resolve(here, 'runs'), output);
if (relativeOutput.startsWith('..') || isAbsolute(relativeOutput)) throw new Error('Acceptance output must stay in validation/runs.');
mkdirSync(output, { recursive: true });
const input = process.env.COHOST_ACCEPTANCE_CONFIG;
const config = input ? JSON.parse(readFileSync(resolve(input), 'utf8')) : {};

export default defineConfig({
  testDir: resolve(here, 'browser'),
  testMatch: '**/*.spec.mjs',
  timeout: 120_000,
  expect: { timeout: 20_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  forbidOnly: true,
  outputDir: resolve(output, 'artifacts'),
  metadata: {
    implementationRevision: config.implementationRevision ?? '',
    engineRevision: config.engineRevision ?? '',
    environmentKind: config.environmentKind ?? '',
    contractSha256: createHash('sha256').update(readFileSync(resolve(here, '../contract.json'))).digest('hex'),
  },
  reporter: [
    ['list'],
    ['json', { outputFile: resolve(output, 'playwright.json') }],
    [resolve(here, 'browser/reporter.mjs'), { output }],
  ],
});
