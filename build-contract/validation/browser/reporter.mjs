import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const contract = resolve(dirname(fileURLToPath(import.meta.url)), '../../contract.json');

export default class AcceptanceReporter {
  constructor({ output }) { this.output = output; this.results = []; }
  onBegin(config) { this.metadata = config.metadata; this.startedAt = new Date().toISOString(); }
  onError() { this.workerFailure = true; }
  onTestEnd(test, result) {
    const id = test.title.match(/^(T\d{3})\b/)?.[1];
    if (!id) return;
    this.results.push({ testId: id, status: result.status,
      screenshots: result.attachments.filter(a => a.contentType === 'image/png' && a.path).map(a => a.path),
    });
  }
  onEnd(result) {
    mkdirSync(this.output, { recursive: true });
    writeFileSync(resolve(this.output, 'browser-results.json'), JSON.stringify({
      schemaVersion: 1, ...this.metadata,
      contractSha256: createHash('sha256').update(readFileSync(contract)).digest('hex'),
      startedAt: this.startedAt, finishedAt: new Date().toISOString(),
      status: this.workerFailure || !this.results.length ? 'failed' : result.status,
      playwrightReportPath: resolve(this.output, 'playwright.json'), results: this.results,
    }, null, 2));
  }
}
