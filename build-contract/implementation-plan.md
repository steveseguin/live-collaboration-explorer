# Implementation plan and AI work order

## Work order

> Build the browser co-host prototype described by this package. Read README, PRD, decisions, integration map, TRD and open review findings before coding. Resolve the documented gate gaps before treating `contract.json` and the checker as sufficient acceptance machinery. Implement only in an authorized checkout. Do not change acceptance thresholds or remove tests to obtain a green result. Report all external dependencies, failed/blocked cases and evidence limitations. Full acceptance requires all required variants and independent media/device/QA evidence.

## Milestones

| Stage | Work | Exit evidence | What the label means |
|---|---|---|---|
| M0 — source and environment | Pin actual implementation HEAD, inspect current contributor guidance/messaging/test rules, baseline original source, prepare local/QA environment and data | Source/build manifests, decisions, contract check | Ready to implement, not a working prototype |
| M1 — feasibility and authority | Pin engine; prove media access/origin policy and current ingest adapter; establish trusted host/invite/owner service | T002/T003/T014/T024/T038 appropriate early evidence | Critical dependencies demonstrated; mock-only results remain laboratory-only |
| M2 — program path | Stable call engine, host/guest tracks, custom canvas, audio buses, actual WHIP output | T006/T008/T009/T010/T013/T035 on independent receiver | Media laboratory working; no claim of mobile/QA completion |
| M3 — product journey | Console launcher/status, guest consent/checks, private text, admission/remove/leave, clear faults | Eight browser cases plus applicable isolation/race checks | Browser workflow demonstrated |
| M4 — window ownership | Independent studio singleton/lease, console reload survival, PiP/fallback/return, cleanup | T017–T021 with headed browsers and receiver continuity | Window/lifetime behavior demonstrated |
| M5 — failure and device behavior | Permission failures, reconnects, devices, direct/TURN, real phones, spoof/replay/secret checks | T005/T012/T015/T022–T033 | Required recovery/device/security conditions demonstrated |
| M6 — integration and endurance | Current host application regression, QA buyer/event/seller context, 30-minute soak, complete evidence ledger | T034/T036–T040 plus all previous variants; completion checker exits 0 | Full prototype accepted only if artifacts support every claim |

The stages organize work; they do not make later acceptance requirements optional. Tests may be run early, and failures should guide implementation. Do not postpone origin/ingest feasibility until after polishing UI.

## Suggested change boundaries for the future implementation

1. Small feature-gated launcher/session-status addition near existing host-console controls.
2. New independent studio page and guest page, with appropriate SSR/auth/bootstrap integration.
3. Trusted control-service adapter with concrete documented endpoint/authorization decisions.
4. VDO.Ninja adapter, compositor/audio router and publisher modules, isolated from commerce state.
5. Floating view and diagnostics modules with explicit ownership cleanup.
6. English locale keys, generated files/flag schema and existing repository checks as required by current contributor guidance.
7. Acceptance evidence and separate harness/config; avoid broad rewrites of the host page or wholesale replacement with an old branch.

These are proposed areas, not authorization to modify the reviewed checkout in this planning task.

## Required engineering decisions before declaring M1 complete

- Exact engine revision and origin/media-access route.
- Real current WHIP endpoint/auth/session/codec contract for the prepared event.
- Trusted host eligibility, guest capability and exclusive owner implementation.
- Browser/device matrix and physical hardware access.
- Independent receiver recording and timing method.
- Studio route/session discovery method after console reload.

An unresolved decision is recorded with its affected test IDs and BLOCKED status. It must not be replaced by a UI mock while retaining a full-completion claim.

## Run and report workflow

1. Run `python validation\verify_contract.py` to verify package/traceability consistency.
2. Configure local exclusions for private outputs; copy `validation\config.example.json` to private configuration and fill explicitly authorized local/QA routes, origins, test event IDs, revisions, fixtures and auth state paths.
3. Install the harness's own dependencies under `validation\`, not the host application. Generate controlled media fixtures there.
4. Execute the supplied browser suite against the implementation. Preserve native Playwright JSON/screenshots/traces in ignored private output.
5. Execute the remaining [scenario procedures](acceptance-tests.md) with the required environment and evidence. Analyze receiver media separately; record exact measurement intervals.
6. Initialize/fill the completion ledger using `validation\completion.py`. Do not prefill `passed` or use illustrative/example evidence as real results.
7. Run the completion checker. Investigate every failure or missing item. Inspect the linked artifacts; schema validation alone cannot prove the artifacts are truthful.
8. Deliver a revision-bound runbook, build manifest, evidence ledger and clear completion label. Redact live credentials/capabilities before sharing artifacts.


## Public scope and references

This is a proposed engineering contract, not an approved product specification or a claim about a deployed system. Internal source maps, source revisions, private research, service locations and run artifacts are intentionally not distributed. See [public studio research](../notes/studio-and-popout.md), [integration responsibilities](integration-map.md), and [open review findings](review-findings.md).

Return to [package overview](README.md).
