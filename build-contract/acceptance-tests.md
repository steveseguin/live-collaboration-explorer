# Acceptance scenarios

All 40 scenarios and 80 variants are required for the proposed full profile. Eight browser cases are supplied; the others are assisted, real-media, device, performance or integration procedures, not fictional automated passes. Read [open review findings](review-findings.md) before treating these procedures or their checker as complete.

## Common setup

Use [validation instructions](validation/README.md), a pinned implementation/engine, and an explicitly authorized non-production event. Never target production, place real bids or make purchases. Host red/440 Hz and guest blue/880 Hz are controlled laboratory fixtures, not physical-device evidence. Receiver evidence must come from an independent receiving path, not a recording of the studio preview.

Declare observation windows, startup grace and injected-fault intervals before analysis; do not discard accidental failures afterward.

## T001 - Console entry, popup failure and singleton launch

**Method:** browser. **Variants:** default. **Requirements:** R001, R004, R005, R034, R049.

Steps:

1. Open a prepared eligible host event with the feature enabled.
2. Activate Open co-host studio twice; inspect the studio and console.
3. Repeat with popup creation denied and inspect recovery guidance.

Pass requirements:

- Listings and buyer chat remain usable.
- One studio/media owner is created; second action focuses it.
- Popup failure is visible and no hidden capture/publisher starts.

Required evidence kinds: `playwright-json, screenshot`.

## T002 - Feature, authorization and event-state rejection

**Method:** assisted-integration. **Variants:** feature-off, unauthorized-host, wrong-event, ended-event, cancelled-event. **Requirements:** R002, R003, R006, R022, R029.

Steps:

1. Try the console entry and direct bootstrap URLs for each variant.
2. Attempt invite/publish operations at the service boundary using the denied principal or event.
3. Inspect network, capture indicators and event state.

Pass requirements:

- Both UI and trusted boundary deny the action.
- Feature-off initializes no VDO.Ninja/capture/output.
- Existing seller-consent and grants remain effective.

Required evidence kinds: `network-summary, screenshot, service-log`.

## T003 - Invite lifecycle and least privilege

**Method:** assisted-integration. **Variants:** valid, wrong-event, expired, revoked, reused, concurrent-redemption, declined. **Requirements:** R003, R007, R008, R009, R010, R043.

Steps:

1. Create an invite for event A; inspect redacted guest bootstrap.
2. Attempt the variant against event B and unauthorized host actions as appropriate.
3. Revoke/rotate/redeem and retry the original link, including simultaneous redemption requests; for declined, explicitly decline before capture.

Pass requirements:

- Only one valid event-bound guest lease is issued.
- Expired/revoked/redeemed capabilities cannot join anew; decline does not capture and clearly exits setup.
- No host/ingest authority or secrets appear in guest data.

Machine-checked measurements:

- `inviteTtlSeconds <= 900`.

Required evidence kinds: `network-summary, service-log, screenshot`.

## T004 - Guest device checks and backstage join

**Method:** browser. **Variants:** default. **Requirements:** R006, R010, R011.

Steps:

1. Use controlled fake host/guest devices in separate browser processes.
2. Open a freshly issued invitation, click Check devices, then Join backstage.
3. Read readiness and guest status in both views.

Pass requirements:

- Nothing captures before an explicit action.
- Actual tracks and transport establish readiness.
- Guest is Backstage; Bring guest on air is shown but remains disabled until output is publishing; no On air label appears yet.

Required evidence kinds: `playwright-json, screenshot`.

## T005 - Permission and device failure recovery

**Method:** assisted-browser. **Variants:** camera-denied, mic-denied, prompt-dismissed, missing-device, busy-device, iframe-policy-denied. **Requirements:** R011, R012.

Steps:

1. Begin guest setup with the selected permission/device failure.
2. Inspect status, available guidance and active tracks.
3. Correct the condition and explicitly retry.

Pass requirements:

- No false Ready or On air state.
- A clear retry/direct-open path is available and capture resources are not leaked.
- Successful retry reaches backstage once.

Required evidence kinds: `screen-recording, diagnostic-export`.

## T006 - Backstage media isolation at independent receiver

**Method:** media. **Variants:** default. **Requirements:** R013, R019.

Steps:

1. Publish the moving red host fixture with a 440 Hz tone; join the moving blue guest fixture with an 880 Hz tone backstage.
2. Record an independent program receiver for at least 15 seconds after stabilization.
3. Analyze the interval excluding only the declared startup grace.

Pass requirements:

- Host video/audio are present.
- Guest video/audio are absent even while host preview/private conversation works.
- Receiver recording, not local UI, is the oracle.

Machine-checked measurements:

- `hostRedMinFraction >= 0.02`.
- `guestBlueMaxFraction <= 0.001`.
- `hostToneMinDbfs >= -35`.
- `guestToneMaxDbfs <= -55`.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline`.

## T007 - Private backstage text

**Method:** browser. **Variants:** default. **Requirements:** R014.

Steps:

1. Join a guest backstage.
2. Send unique text from the host and a reply from the guest using Private message.
3. Inspect both private conversations and the visible public buyer chat region.

Pass requirements:

- Both private participants see the text once.
- Public buyer chat does not show either message.
- Labels clearly identify the private conversation.

Required evidence kinds: `playwright-json, screenshot`.

## T008 - Admission and true public program transition

**Method:** media. **Variants:** default. **Requirements:** R001, R013, R015, R019, R027.

Steps:

1. Begin in the T006 state with independent recording active.
2. Host clicks Bring guest on air and records the command/program revision time.
3. Inspect guest acknowledgement and the stabilized receiver interval.

Pass requirements:

- Guest becomes On air only after admission acknowledgement.
- Red host and blue guest plus both tones reach the real program.
- Publisher/session IDs and original seller remain unchanged.

Machine-checked measurements:

- `hostRedMinFraction >= 0.02`.
- `guestBlueMinFraction >= 0.01`.
- `hostToneMinDbfs >= -35`.
- `guestToneMinDbfs >= -35`.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline, diagnostic-export`.

## T009 - All program layouts without republishing

**Method:** media. **Variants:** stacked, side-by-side, picture-in-picture. **Requirements:** R016.

Steps:

1. Admit the marked guest and keep independent recording active.
2. Select the required layout.
3. Compare fit/crop/labels, output dimensions and session/track IDs before and after.

Pass requirements:

- Layout matches its name and both source identities remain visible.
- Output remains exactly 720x1280.
- No camera reacquisition, publisher restart or duplicate audio.

Machine-checked measurements:

- `width == 720`.
- `height == 1280`.
- `publisherSessionChanges == 0`.

Required evidence kinds: `receiver-recording, media-analysis, screenshot, diagnostic-export`.

## T010 - Camera/mic controls and program audio buses

**Method:** media. **Variants:** guest-mic, host-program-mute, guest-camera, host-camera-exclusion. **Requirements:** R017, R018, R019, R036.

Steps:

1. While on air, independently operate guest self-mute/camera and host program exclusion.
2. Record receiver intervals for each action; inspect caller return and local consent state.
3. Restore the permitted state explicitly.

Pass requirements:

- Mute excludes the selected public voice without doubling another voice.
- Camera exclusion shows a placeholder rather than frozen guest video.
- Host cannot force a guest physical capture on after local denial/mute.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline, screen-recording`.

## T011 - Removal and voluntary leave

**Method:** media. **Variants:** host-removes, guest-leaves. **Requirements:** R010, R020, R021.

Steps:

1. Admit marked guest with independent recording/timeline active.
2. Perform the variant.
3. Measure exclusion at program ingress, inspect guest state and original publisher continuity.

Pass requirements:

- Guest media is excluded within 1000 ms of the acknowledged command.
- Original host continues without a publisher restart.
- Leave stops guest capture; removal invalidates the previous admission/lease.

Machine-checked measurements:

- `programExclusionMs <= 1000`.
- `publisherSessionChanges == 0`.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline, diagnostic-export`.

## T012 - Capacity, repeated joins and replacement

**Method:** browser. **Variants:** default. **Requirements:** R001, R005, R008, R009, R044.

Steps:

1. Join one guest backstage.
2. Attempt the redeemed invitation from a separate browser session; trusted concurrent redemption/capacity is additionally exercised in T003.
3. Remove the first guest, issue a fresh invitation and join the replacement; retry the old page.

Pass requirements:

- Second contribution is rejected without disturbing the first.
- Replacement reaches backstage after explicit removal.
- Old guest cannot regain on-air status by retrying.

Required evidence kinds: `playwright-json, screenshot`.

## T013 - Actual custom canvas/audio publishing pipeline

**Method:** media. **Variants:** default. **Requirements:** R016, R019, R023, R024, R027, R045.

Steps:

1. Start publishing from our studio with marked source fixtures.
2. Inspect the selected output tracks and independent receiver.
3. Verify local preview is identified separately from delayed audience playback and no tab-share/OBS/virtual-camera dependency is used.

Pass requirements:

- The video source is the custom canvas and audio source is the explicit program bus.
- Independent receiver contains intended media.
- Capture, output bytes and receiver evidence agree.

Required evidence kinds: `receiver-recording, media-analysis, diagnostic-export, network-summary`.

## T014 - WHIP negotiation and session resource lifecycle

**Method:** protocol-integration. **Variants:** controlled-protocol, real-ingest. **Requirements:** R025, R026.

Steps:

1. Acquire event-authorized WHIP configuration.
2. Start and stop publishing against the selected receiver, capturing a redacted protocol summary.
3. Exercise response/ICE failure handling without creating duplicate sessions.

Pass requirements:

- Observe offer/answer, successful session acquisition and resource URL, and actual media for the real-ingest variant.
- Explicit stop attempts authenticated session DELETE.
- Protocol fixture success alone does not establish real ingest compatibility.

Machine-checked measurements:

- `postStatus == 201`.
- `resourceLocationPresent == true`.
- `deleteAttempted == true`.

Required evidence kinds: `network-summary, diagnostic-export, service-log`.

## T015 - Endpoint rotation and expired authorization

**Method:** assisted-integration. **Variants:** endpoint-updated, authorization-expired, no-whip. **Requirements:** R025, R028, R037.

Steps:

1. Publish against prepared event endpoint A.
2. Rotate the event endpoint or invalidate its authorization using the test control service.
3. Observe the existing endpoint-update flow, fresh authorization and bounded reconnect.

Pass requirements:

- No indefinite obsolete endpoint/token retries.
- Program remains bound to the original event; unsupported/no-WHIP configuration is a clear fault.
- Fresh endpoint is used only after trusted resolution.

Machine-checked measurements:

- `unboundedRetryObserved == false`.

Required evidence kinds: `network-summary, service-log, event-timeline, diagnostic-export`.

## T016 - Publishing versus event lifecycle

**Method:** browser. **Variants:** default. **Requirements:** R029, R058.

Steps:

1. Use a prepared non-production event; record event state and original Start/End controls.
2. Start then stop publishing from the studio.
3. Inspect event state and action traffic; exercise a prepared ended-event transition separately in integrated validation.

Pass requirements:

- Publishing start/stop alone does not start/end the seller event.
- Existing event consent and start/end actions remain separate.
- No purchase, bid or real commerce action is performed.

Required evidence kinds: `playwright-json, screenshot`.

## T017 - Console navigation, reload and event binding

**Method:** browser. **Variants:** default. **Requirements:** R004, R030.

Steps:

1. Launch the studio and join a guest.
2. Switch console tabs, then reload the console.
3. Navigate the console to a different prepared event and inspect the original studio/session.

Pass requirements:

- Studio and media owner persist.
- Session stays bound to event A and is never retargeted to event B.
- Existing listings/chat controls remain available.

Required evidence kinds: `playwright-json, screenshot`.

## T018 - Real Document PiP and fallback

**Method:** headed-browser. **Variants:** chrome, edge, unsupported-or-denied. **Requirements:** R031.

Steps:

1. Launch a studio in the chosen host browser.
2. Activate Float studio from a top-level user gesture.
3. Exercise unavailable/denied PiP in the fallback variant.

Pass requirements:

- Supported browser creates an actual always-on-top Document PiP view with usable controls.
- Unsupported/denied path stays usable in the ordinary studio window.
- No embedded iframe attempts to invoke the API as top-level.

Required evidence kinds: `screen-recording, screenshot, diagnostic-export`.

## T019 - PiP continuity and normal console interaction

**Method:** media. **Variants:** chrome, edge. **Requirements:** R005, R016, R031, R032, R033, R053.

Steps:

1. Admit moving/audio-marked guest and record an independent receiver.
2. Float/return ten times while using listings/chat and switching focus.
3. Observe engine/session/track IDs, output motion and active publisher counts.

Pass requirements:

- No live iframe reload/reparent, duplicate camera or session.
- Program continues at acceptance frame rate without a freeze over 1000 ms.
- Floating control actions affect the same program.

Machine-checked measurements:

- `decodedFps >= 25`.
- `maxFreezeMs <= 1000`.
- `engineGenerationChanges == 0`.
- `publisherSessionChanges == 0`.
- `floatReturnCycles >= 10`.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline, screen-recording, diagnostic-export`.

## T020 - PiP close is not studio stop

**Method:** media. **Variants:** browser-close, return-control. **Requirements:** R032, R033, R052.

Steps:

1. Record the program with the guest on air in a floated view.
2. Close PiP through browser chrome, then repeat using Return studio.
3. Inspect restoration, output continuity and resource ownership.

Pass requirements:

- Controls/rendering restore to the ordinary studio within 1000 ms.
- Original engine/publisher continue and local capture remains owned once.
- Final Stop publishing remains a separate action.

Machine-checked measurements:

- `restoreMs <= 1000`.
- `publisherSessionChanges == 0`.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline, diagnostic-export`.

## T021 - Studio stop, close and lost-owner cleanup

**Method:** assisted-integration. **Variants:** normal-stop, normal-close, cancel-close, crash-or-lost-owner. **Requirements:** R026, R030, R034, R052.

Steps:

1. Publish and join a guest.
2. Exercise explicit stop/normal close, cancel-close where browser permits, and process-crash/lost-owner lease variants.
3. Observe capture indicators, receiver end, session DELETE, listeners and owner expiry.

Pass requirements:

- Normal final stop leaves no owned capture/output resources.
- Cancelled close preserves output.
- Crash/lost-owner lease expires within 10000 ms; returning views cannot revive it.

Required evidence kinds: `screen-recording, diagnostic-export, network-summary, service-log`.

## T022 - Guest loss and explicit re-admission

**Method:** fault-injection. **Variants:** default. **Requirements:** R013, R035, R037.

Steps:

1. Admit a guest and record program/timeline.
2. Interrupt only guest connectivity/tracks for at least three seconds.
3. Restore connectivity and inspect setup/backstage before trying a new admission.

Pass requirements:

- Loss detection plus exclusion takes at most 3000 ms.
- Stale/frozen guest is replaced by host-only/placeholder output.
- Recovered guest is backstage, never automatically on air.

Machine-checked measurements:

- `lossToExclusionMs <= 3000`.
- `automaticReadmissions == 0`.

Required evidence kinds: `receiver-recording, media-analysis, event-timeline, diagnostic-export`.

## T023 - Host/output transport faults and bounded retries

**Method:** fault-injection. **Variants:** network-loss, receiver-errors. **Requirements:** R028, R037.

Steps:

1. Publish against the controlled ingest.
2. Interrupt output connectivity or return retryable signaling errors.
3. Measure attempts, backoff and stable fault; explicitly request recovery.

Pass requirements:

- At most three automatic retries at 1/2/4 seconds plus bounded jitter.
- Stable fault is actionable and truthful.
- Recovery keeps event binding and guest admission safe.

Machine-checked measurements:

- `automaticRetries <= 3`.
- `automaticReadmissions == 0`.

Required evidence kinds: `network-summary, event-timeline, diagnostic-export`.

## T024 - Real direct and TURN-relayed contribution

**Method:** network-integration. **Variants:** direct, forced-relay. **Requirements:** R038.

Steps:

1. Use separate host/guest network endpoints with declared ICE configuration.
2. Force the selected connectivity route.
3. Join, converse, admit and capture selected ICE candidate-pair plus real output evidence.

Pass requirements:

- Actual selected candidate type demonstrates the route, not just a TURN URL in configuration.
- Media/admission work through the route.
- Missing TURN service is BLOCKED, not a pass.

Machine-checked measurements:

- `selectedCandidateType in ["host", "srflx"]` (variants: direct).
- `selectedCandidateType == "relay"` (variants: forced-relay).

Required evidence kinds: `receiver-recording, diagnostic-export, network-summary`.

## T025 - Physical mobile guest happy path

**Method:** real-device. **Variants:** android-chrome, iphone-safari. **Requirements:** R010, R017, R021, R039, R059.

Steps:

1. Use a physical supported phone over HTTPS and a headed desktop host.
2. Follow an invitation through consent, permissions, checks, backstage, admission and controls.
3. Leave and verify capture indicators stop; record device/browser/OS versions.

Pass requirements:

- All critical controls work on the actual phone.
- Identity, private/on-air state and seller boundaries remain clear.
- No emulation is presented as physical-device evidence.

Machine-checked measurements:

- `physicalDevice == true`.

Required evidence kinds: `screen-recording, receiver-recording, device-record, diagnostic-export`.

## T026 - Mobile orientation, camera and suspension lifecycle

**Method:** real-device. **Variants:** android-chrome, iphone-safari. **Requirements:** R035, R040.

Steps:

1. Begin with the physical guest on air.
2. Rotate and switch cameras, then background/lock and foreground the guest.
3. Record platform mute/end/suspension events and public output.

Pass requirements:

- Controls remain usable through orientation/device change.
- Observed suspension/mute/end gates guest media within 2000 ms.
- Resume requires checks/backstage and explicit re-admission.

Machine-checked measurements:

- `observedSuspensionToExclusionMs <= 2000`.
- `automaticReadmissions == 0`.

Required evidence kinds: `screen-recording, receiver-recording, device-record, event-timeline, diagnostic-export`.

## T027 - Unsupported capabilities and direct-open recovery

**Method:** assisted-browser. **Variants:** no-canvas-capture, unsupported-host, blocked-guest-embed. **Requirements:** R012, R041.

Steps:

1. Run with the selected unsupported capability or blocked embed.
2. Attempt setup/publishing.
3. Follow the offered supported-browser/direct-open path.

Pass requirements:

- The limitation is explained without fake Ready/Publishing status.
- No stuck camera or output session remains.
- Supported recovery preserves event/session authorization.

Required evidence kinds: `screenshot, diagnostic-export, network-summary`.

## T028 - Message origin, schema and privilege rejection

**Method:** browser. **Variants:** default. **Requirements:** R003, R022, R042, R047, R051.

Steps:

1. Create a valid studio session with read-only diagnostics enabled.
2. Send controlled malformed/cross-event/stale/untrusted-source messages into its message boundary.
3. Compare diagnostics and visible guest/output state before and after.

Pass requirements:

- All forged commands are rejected without media/program/commerce mutation.
- No test-only hook bypasses trusted authorization.
- Existing player commerce buses remain separate.

Required evidence kinds: `playwright-json, screenshot`.

## T029 - Command races and generation invalidation

**Method:** assisted-integration. **Variants:** admit-remove-race, duplicate-request, old-generation. **Requirements:** R009, R015, R020, R042, R044.

Steps:

1. Race admit/remove, retry a duplicate request ID and reorder acknowledgements.
2. Replace or reconnect the guest.
3. Replay old-generation admit/control messages and observe the program.

Pass requirements:

- Removed/replaced guest never returns on air.
- Commands are idempotent and stale generations are rejected.
- Acknowledgements identify the applied program revision.

Required evidence kinds: `event-timeline, service-log, receiver-recording, diagnostic-export`.

## T030 - Credential isolation and redacted evidence

**Method:** assisted-integration. **Variants:** default. **Requirements:** R007, R014, R022, R043.

Steps:

1. Use distinctive synthetic host/ingest secret canaries and expired disposable invites.
2. Inspect guest network/DOM/storage, host persistent storage, analytics and exported logs.
3. Review evidence before sharing; remove/redact live capabilities.

Pass requirements:

- Host/ingest secrets never cross into guest/public surfaces or persistent stores.
- Sensitive URLs and payloads are redacted from shareable diagnostics.
- Media traces/artifacts remain in ignored private output directories.

Machine-checked measurements:

- `hostSecretLeaks == 0`.

Required evidence kinds: `network-summary, secret-scan-report, diagnostic-export`.

## T031 - Keyboard, focus and assistive presentation

**Method:** accessibility. **Variants:** default. **Requirements:** R048.

Steps:

1. Complete the critical host/guest flow with keyboard only.
2. Float/return/close PiP and trigger a recoverable error.
3. Inspect names, focus order, status announcements and private-message presentation with assistive tooling.

Pass requirements:

- Every critical control is reachable/operable and focus returns predictably.
- State is not conveyed by color alone.
- Private messages are not announced into public chat.

Required evidence kinds: `screen-recording, accessibility-report, screenshot`.

## T032 - Critical viewport layouts

**Method:** browser. **Variants:** default. **Requirements:** R004, R049.

Steps:

1. At 1280x720 inspect console listings/public chat/co-host entry and studio controls.
2. At 360x640 inspect the guest setup/backstage/on-air controls.
3. Traverse visible controls and inspect horizontal overflow.

Pass requirements:

- Critical controls are visible, usable and not clipped.
- Guest viewport has no horizontal document overflow.
- Host co-host entry does not obscure listings or buyer chat.

Required evidence kinds: `playwright-json, screenshot`.

## T033 - Host camera/microphone loss and switch

**Method:** assisted-browser. **Variants:** camera, microphone. **Requirements:** R017, R036.

Steps:

1. Publish while the guest is admitted.
2. Remove/switch the selected host input or deny its renewed permission.
3. Observe program placeholder/silence, error recovery and active track counts.

Pass requirements:

- State reflects actual device availability; no frozen success state.
- Retry/switch is explicit and restores only permitted capture.
- No duplicated host tracks/audio.

Required evidence kinds: `receiver-recording, diagnostic-export, screen-recording`.

## T034 - Thirty-minute media and interaction soak

**Method:** performance-media. **Variants:** default. **Requirements:** R005, R033, R052, R053, R055.

Steps:

1. Use the declared desktop hardware/browser and moving source fixtures; record continuous receiver output and samples.
2. Warm up five minutes, then exercise chat/listings/layouts/float/return during a total run of at least 1800 seconds.
3. Compare post-warmup and final five-minute median renderer heap; inspect source motion and queues.

Pass requirements:

- At least 25 decoded fps and no unplanned source-motion freeze over 1000 ms under normal operation.
- At most one publisher and bounded frame queues.
- JS heap median growth is no more than 100 MiB.

Machine-checked measurements:

- `soakSeconds >= 1800`.
- `decodedFps >= 25`.
- `maxFreezeMs <= 1000`.
- `heapGrowthMiB <= 100`.
- `maxProgramPublishers <= 1`.

Required evidence kinds: `receiver-recording, media-analysis, performance-report, event-timeline, diagnostic-export`.

## T035 - A/V alignment, conversational delay and echo

**Method:** timing-media. **Variants:** default. **Requirements:** R018, R023, R054.

Steps:

1. Use synchronized visible flash/audio-pulse fixtures and a declared controlled network of at most 20 ms added RTT and no induced loss.
2. Collect at least 30 observations of call and local-program timing.
3. Exercise headphones and normal speaker echo cancellation; record audience delay separately.

Pass requirements:

- p95 A/V skew <=150 ms, one-way call delay <=750 ms and local-program receiver delay <=2000 ms.
- No sustained self-return/doubled voice; no delayed buyer audio in the call.
- Wall clocks/timelines are synchronized or uncertainty is bounded and reported.

Machine-checked measurements:

- `avSkewP95Ms <= 150`.
- `callOneWayP95Ms <= 750`.
- `localProgramP95Ms <= 2000`.
- `timingObservations >= 30`.

Required evidence kinds: `receiver-recording, media-analysis, timing-report, event-timeline`.

## T036 - Integrated QA buyer program and commerce context

**Method:** qa-integration. **Variants:** default. **Requirements:** R001, R014, R022, R023, R025, R029, R054, R056, R058, R059.

Steps:

1. Use an explicitly authorized prepared QA event and original seller/item; start event only through existing consent/controls if needed.
2. Observe actual buyer playback while admitting/removing guest and changing layouts.
3. Send unique private host/guest messages; inspect a separate buyer session and its chat/network traffic throughout a declared observation window.
4. End the prepared event through its existing control and observe studio teardown.

Pass requirements:

- At least two program revisions reach the real buyer with the original event/seller/item.
- Neither private message reaches buyer chat, buyer message payloads or program overlays; console-only absence is insufficient.
- Publishing and event lifecycle stay distinct; no bid/purchase is executed.
- Ended event denies new admission and tears down output within 5000 ms of detection.

Machine-checked measurements:

- `buyerProgramTransitions >= 2`.
- `privateMessageBuyerLeaks == 0`.
- `sellerMismatchCount == 0`.
- `eventEndDetectedToStopMs <= 5000`.

Required evidence kinds: `buyer-recording, network-summary, event-timeline, service-log, screenshot`.

## T037 - Current host application regression and integration conventions

**Method:** integration-review. **Variants:** default. **Requirements:** R002, R004, R006, R050, R051, R060.

Steps:

1. Review the implementation diff against the pinned current integration map and current contributor/testing/messaging guides.
2. Exercise feature-off host console and enabled listing/chat/consent/event controls; run appropriate existing build/type/i18n/generated-file checks in the implementation checkout.
3. Inspect SSR and messaging integration; record pre-existing failures separately.

Pass requirements:

- Feature-off behavior and existing seller workflows are preserved.
- Context/grants, English i18n/codegen, logger and browser/server boundaries are respected.
- Historical experiment code is not blindly restored over current source.

Required evidence kinds: `diff-review, build-report, screen-recording, network-summary`.

## T038 - Pinned engine, origin policy and deployment feasibility

**Method:** deployment-integration. **Variants:** default. **Requirements:** R012, R024, R041, R045, R046.

Steps:

1. Record implementation/engine revisions and actual served origins/headers.
2. Verify the selected same-origin media-access or explicit frame/audio bridge path.
3. Exercise camera/mic iframe delegation and custom-canvas output without screen sharing.

Pass requirements:

- Origin/policy assumptions are demonstrated in the actual deployment.
- Alpha/release source is pinned or vendored, not an unversioned moving dependency.
- Browser/canvas support is truthful and no cross-origin DOM access is assumed.

Machine-checked measurements:

- `enginePinVerified == true`.

Required evidence kinds: `build-manifest, network-summary, receiver-recording, diagnostic-export`.

## T039 - Independent evidence and truthful diagnostics

**Method:** evidence-review. **Variants:** default. **Requirements:** R011, R015, R027, R046, R047, R057.

Steps:

1. Compare application diagnostics with output network counters and independent receiver/buyer artifacts.
2. Confirm telemetry has no mutating acceptance backdoor or fabricated success counter.
3. Check timestamps, generation and program revisions across evidence.

Pass requirements:

- Preview, call transport, program output and audience confirmation are separately proven.
- Read-only telemetry agrees with independent observations.
- Missing dependencies/results remain blocked or not_run.

Required evidence kinds: `diagnostic-export, network-summary, receiver-recording, evidence-review`.

## T040 - Reproducible handoff and unchanged review checkout

**Method:** handoff-review. **Variants:** default. **Requirements:** R057, R058, R059, R060.

Steps:

1. Inspect setup commands, decisions, contract traceability and all required case variants.
2. Compare the source snapshot with its review baseline, explicitly reporting scope/unreadable files.
3. Confirm future implementation is isolated and completion claims match evidence.

Pass requirements:

- No edits were made to the inspected host application source by this review package.
- Commands and dependencies are reproducible.
- Mobile-web scope and deferred features are documented; no skipped/missing result is promoted to accepted.

Required evidence kinds: `source-comparison, build-manifest, evidence-review`.

Return to [package overview](README.md).
