# External acceptance tools

**These tools do not implement the co-host product.** The [open review findings](../review-findings.md) remain unresolved. A completion-checker exit code alone is not a sufficient acceptance decision.

## Supplied tools

- `verify_contract.py`: package documents, links, traceability and eight-browser-case agreement.
- `browser/studio.spec.mjs`: eight executable workflows for a future application's accessible UI and read-only diagnostics.
- `generate_fixtures.py`: distinguishable moving host/guest cameras and 440/880 Hz laboratory audio.
- `analyze_media.py`: partial independent recording oracle for color/tone presence and dimensions.
- `completion.py`: initialize an unexecuted ledger, import browser results and check coverage/evidence/metric rules, subject to the documented gaps.
- `snapshot_source.py`: read-only source hashes and revision metadata, with output outside the inspected checkout.
- `validate_toolchain.py`: tooling-only negative checks and synthetic media roundtrip; never product acceptance.

The remaining 32 scenarios are assisted/manual/device/media/integration procedures in [acceptance scenarios](../acceptance-tests.md), not supplied automated tests.

## Setup and isolation

Use Python 3.11+, Node 20+, the pinned Playwright dependency, and trusted FFmpeg/ffprobe for media checks. Run these commands from `build-contract\validation`:

```powershell
npm ci --ignore-scripts --no-audit --no-fund
python verify_contract.py
npm run list
```

Actual browser execution also needs an installed supported Chromium browser:

```powershell
npx playwright install chromium
```

No command starts the application, installs dependencies in a target checkout, or infers an application URL. Discovery is not product execution.

Keep `runs`, `.auth`, `fixtures-generated`, `node_modules` and `__pycache__` private and out of commits. Configure local Git exclusions before generating outputs; do not assume this public package adds or changes repository ignore rules. Only authored tool source, the example config and dependency manifests belong in public commits.

## Configuration and authorized targets

Copy `config.example.json` to `runs\config.json` and replace all placeholders:

```powershell
New-Item -ItemType Directory -Force runs | Out-Null
Copy-Item config.example.json runs\config.json
$env:COHOST_ACCEPTANCE_CONFIG = (Resolve-Path runs\config.json).Path
```

Provide two prepared event IDs/console URLs; exact application/guest and engine origins; actual implementation/engine revisions; generated host/guest fixture paths; and optional private authorized auth state. Never put credentials into the public example.

The public guard permits loopback and reserved `.test` lab hosts only; non-loopback hosts require HTTPS. A real QA deployment needs an explicitly reviewed non-production host-policy adaptation in `browser/support.mjs`, actual authorization, and prepared test accounts/events. No production publication, bid or purchase is authorized by this package.

The publisher case needs a functioning test WHIP receiver and trusted adapter. Missing config/services/controls fail rather than silently substituting mocks or the illustrative explorer.

## Accessible UI contract

English is the acceptance locale. These names are proposed future UI contracts, not claims about an existing platform:

| Surface | Accessible role/name | Behavior |
|---|---|---|
| Console | button `Open co-host studio` | Launch/focus the event-bound studio; blocked popup produces an alert |
| Console | regions `Listing management`, `Public buyer chat`; tab `Listings` | Existing workflows remain usable |
| Studio | region `Co-host studio` | Top-level media-owner shell |
| Studio | button `Prepare host`; status `Host readiness` | Explicit device preparation; `Ready` requires actual readiness |
| Studio | button `Create guest invite`; textbox `Guest invitation link` | Guest-only event/session capability |
| Studio/guest | status `Guest status` | Truthful `Backstage`, `On air`, `Removed` and recovery states |
| Studio | buttons `Bring guest on air`, `Remove guest` | Admission requires readiness and publication; removal invalidates old admission |
| Studio | buttons `Start publishing`, `Stop publishing`; status `Publishing status` | `Publishing`/`Stopped` independent of event Start/End |
| Studio | combobox `Program layout` | Stacked, Side by side, Picture in picture |
| Studio | buttons `Float studio`, `Return studio` | Optional floating view of the same media session |
| Guest | region `Join as guest`; button `Decline invitation` | Identity/consent without automatic capture |
| Guest | button `Check devices`; status `Device readiness` | `Ready` requires usable tracks and transport |
| Guest | buttons `Join backstage`, `Leave show` | Explicit guest lifecycle |
| Studio/guest | region `Backstage conversation`; textbox `Private message`; button `Send private message` | Private messages, no public fanout |
| Failures | alert | Actionable permission/device/invite/capacity/recovery guidance |

The public T016 request probe uses proposed `StartEvent`/`EndEvent` operation names. Adapt it to the target application's actual lifecycle adapter without weakening the prohibition on automatic event mutations.

## Read-only diagnostics

In explicitly enabled local/QA acceptance mode, provide `window.__COHOST_DIAGNOSTICS__.snapshot()` on the relevant studio, guest and console surfaces. No mutating force-state functions or authorization bypasses.

```text
schemaVersion: 1
eventId, eventState, sessionId, engineInstanceId, engineGeneration
programRevision, programPublishers, publisherSessionId, publishingState
activeCaptureTrackCount, usableVideoTracks, usableAudioTracks
contributionTransportState, rejectedMessages
guest: { id, generation, state, admitted }  // null before a guest exists
```

Counters are nonnegative integers; states are nonempty strings. Unavailable identifiers are explicit null, not omitted. An open studio has nonempty session/engine identifiers. Additional scenarios need frame/queue/bytes/lease/fault timestamps and telemetry described in the TRD.

Diagnostics correlate observations; they cannot replace receiver recordings, physical devices, authorization checks or independent timing.

## Fixtures and browser workflows

```powershell
python generate_fixtures.py --ffmpeg "C:\path\to\ffmpeg.exe"
npm run test:browser
```

Host and guest use separate browser processes because fake-device file flags are process-wide. Defaults are small 320x240/30fps workflow inputs. Declare production-sized fixtures for performance work, for example `--width 720 --height 1280 --seconds 4 --force`. Emulation and fake devices are laboratory evidence only.

## Independent receiver and analysis

Use a separate authorized receiver that records the actual published audio/video, not the studio DOM or preview. Record its tool, stream identity and predeclared interval.

```powershell
python analyze_media.py runs\my-run\receiver.webm --ffmpeg "C:\path\to\ffmpeg.exe" --ffprobe "C:\path\to\ffprobe.exe" --start 5 --duration 15 --implementation-revision REPLACE_WITH_ACTUAL_HEX_REVISION --engine-revision REPLACE_WITH_ACTUAL_HEX_REVISION --out runs\my-run\backstage-analysis.json
```

The analyzer requires real audio/video, an adequate interval and pinned revisions. It measures color/tone identity and dimensions, not decoded FPS, freezes, layout geometry, A/V skew, echo, device behavior or one-way delay. Follow the additional [measurement procedures](../evidence-and-completion.md).

`--purpose tool-self-check` labels synthetic analyzer testing, never product evidence. The separate tooling self-check is:

```powershell
python validate_toolchain.py --ffmpeg "C:\path\to\ffmpeg.exe" --ffprobe "C:\path\to\ffprobe.exe"
```

Its intentionally missing-target browser run must fail. Synthetic roundtrip success establishes tooling behavior only.

## Ledger and completion

```powershell
python completion.py init --out runs\my-run\ledger.json
python completion.py import-browser runs\my-run\ledger.json runs\browser\browser-results.json
python completion.py check runs\my-run\ledger.json
```

Initialization creates all 80 variants as `not_run`. Fill actual run metadata and execute the scenarios before entering results. Each artifact needs a relative path and SHA-256. Measurement reports need tool identity, implementation/engine revisions, contract hash and metrics; independent media reports also reference an attached receiver recording.

Exit 0 means the current structural checker accepted the ledger; 1 means incomplete/failed evidence; 2 means invalid input/tool error. **Because the [review findings](../review-findings.md) remain open, exit 0 does not establish full acceptance.** Independently inspect provenance, measurement source and actual artifacts.

## Read-only source comparison

The snapshot helper never runs builds, filters or checkout operations in the inspected repository. Use the same explicit scope both times and write outside it:

```powershell
python snapshot_source.py "C:\path\to\host-application" --tracked-only --prefix src/ --prefix package.json --out runs\review\before.json
python snapshot_source.py "C:\path\to\host-application" --tracked-only --prefix src/ --prefix package.json --out runs\review\after.json --compare runs\review\before.json
```

Do not describe selected-prefix equality as a whole-filesystem audit. Report unreadable files and concurrent changes; never revert another person's work.

## References

Public browser/protocol references are in [studio research](../../notes/studio-and-popout.md) and [TRD](../trd.md). Return to [package overview](../README.md).
