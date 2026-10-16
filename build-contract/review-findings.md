# Open review findings

Review date: October 16, 2026. **These findings remain open.** Publishing the public-safe package does not fix them or establish a working product. They are gaps in the contract/tooling, not vulnerabilities established in a deployed service.

## 1. Reports without metrics bypass some provenance checks

`validation/completion.py` checks report revisions and self-check purpose through its measurement-report path. Diagnostic and other reports without a `metrics` object can avoid those checks.

A negative review fixture counted a T005 variant as passing despite an attached diagnostic report identifying different implementation/engine/contract hashes and a self-check purpose. Other unexecuted variants still prevented overall acceptance.

Required follow-up: validate report provenance independently of measurement presence, require the relevant artifact metadata, and add regression cases for stale non-measurement evidence.

## 2. Some independent measurements can come from app diagnostics

The checker constrains color/tone/dimension metrics to media-analysis reports, but other metrics can match any recognized measurement report. A T019 negative fixture satisfied decoded FPS and maximum freeze using a diagnostic export with no receiver-bound measurements.

Required follow-up: define permitted evidence sources per metric. Decoded FPS, source freezes and media timing must come from independent, receiver-bound analysis rather than the application grading itself.

## 3. Owner expiry does not yet define publish-session fencing

An exclusive service lease is not by itself a guarantee that an old WHIP connection stops. A studio could lose only control-service connectivity, retain ingest connectivity, lose its lease, and continue publishing while another studio takes ownership.

Required follow-up: specify how expired/revoked owners lose publication authority, preferably enforced at the ingest/session boundary. Test a control-plane-only network partition, takeover by another browser, and restoration of the old client. A process crash is not the same test.

## 4. Console reload is tested before publication starts

The supplied T017 browser case joins a guest backstage and compares identifiers after console reload/navigation. It does not start a publisher, so it cannot prove uninterrupted broadcast delivery through those actions.

Required follow-up: publish during the reload/navigation scenario, preserve the publisher/session identity, and observe independent receiver progress across the transitions.

## Interpretation

These findings do not erase the usefulness of the proposed requirements or the tools. They limit what a passing result currently proves. Product acceptance requires actual case execution, independent artifact review, and resolution of these gaps; structural checks are not sufficient.

Return to [package overview](README.md).
