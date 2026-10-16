# High-level implementation pseudocode

## Interpretation

This is architecture guidance, not copy/paste host application code. Names describe proposed interfaces. Resolve them against current source and actual authorized services before implementation. Follow the current repository's Result/state/context/export conventions. Requirement IDs and tests remain normative in [contract.json](contract.json).

## Data model

```typescript
type GuestState =
  | { phase: 'absent' }
  | { phase: 'invited'; inviteId: string; expiresAt: number }
  | { phase: 'checking'; guestId: string; generation: number }
  | { phase: 'backstage'; guestId: string; generation: number; readiness: ReadyTracks }
  | { phase: 'admitted'; guestId: string; generation: number; programRevision: number }
  | { phase: 'interrupted'; guestId: string; generation: number; reason: SafeErrorCode }
  | { phase: 'removed'; guestId: string; invalidatedGeneration: number };

type OutputState =
  | { phase: 'idle' }
  | { phase: 'resolving' }
  | { phase: 'negotiating'; attempt: number }
  | { phase: 'publishing'; publisherSessionId: string; startedAt: number }
  | { phase: 'retrying'; attempt: number; nextAttemptAt: number }
  | { phase: 'fault'; code: SafeErrorCode; canRetry: boolean }
  | { phase: 'stopped' };

type ProgramState = {
  eventId: string; sessionId: string; ownerEpoch: number;
  revision: number; layout: 'stacked' | 'side-by-side' | 'picture-in-picture';
  host: SourceHandle;
  guest: null | { source: SourceHandle; generation: number; admitted: boolean };
  hostProgramMuted: boolean; guestProgramMuted: boolean;
};
// SourceHandle/ReadyTracks are opaque media handles, never serialized into a capability URL.
```

## Console launch (R002–R006, R030)

```text
on Open co-host studio click:
    read current event/auth/flags through host application context
    if feature disabled or event ineligible:
        show truthful unavailable state; do not initialize engine/capture
        return

    open/focus a named ordinary studio window synchronously from user gesture
    if popup blocked:
        show Allow pop-ups / Open studio guidance
        return without media initialization

studio bootstrap:
    authorize this host and event through trusted service
    acquire exclusive owner lease, or attach/focus known existing owner
    show studio shell without device access
    start scoped owner/status synchronization
    // Console reload/navigation changes its own view only.
    // Never infer authority from a window name, localStorage value or URL eventId.
```

## Prepare host / guest (R006–R014)

```text
on Prepare host click:
    initialize pinned engine iframe once in fixed studio document
    delegate only required permissions
    ask engine to acquire selected host devices through its supported capture flow
    receive actual track readiness and transport events
    expose local preview; keep publisher idle until explicit Start publishing

on Create guest invite:
    service validates owner lease and event
    atomically issue guest-only capability, TTL <= 900 seconds before redemption
    show copyable guest URL containing no host/ingest authority

guest invite page load:
    resolve safe event/host identity; show explanation, no capture
on Check devices click:
    redeem capability atomically for one guest lease or show explicit rejection
    initialize guest iframe, request devices, establish contribution/conversation
    Ready requires usable tracks AND transport, not iframe.onload
on Join backstage click:
    validate lease/generation and readiness
    attach source to host preview/conversation only
    close guest public video/audio gates
    show Backstage; enable private text channel
```

The exact redemption versus permission-check ordering may vary if the service can reserve/release a short preparation lease. It must retain atomic capacity, expiry, no automatic capture and recoverable denial behavior. Single-use redemption must not accidentally lock a legitimately retrying guest out without an explicit resume lease.

## Program construction (R016–R024)

```text
create program once per owner:
    canvas.width = 720; canvas.height = 1280
    videoTrack = canvas.captureStream(30).videoTrack
    audioContext = create Web Audio context after user action
    audioDestination = audioContext.createMediaStreamDestination()
    connect one host mic source to program gain -> destination
    connect guest mic source to guestProgramGain (initially zero) -> destination
    outgoing = MediaStream([videoTrack, audioDestination.audioTrack])

render next frame:
    snapshot current committed ProgramState
    draw host or deliberate camera-off placeholder
    if guest admitted AND source generation matches ProgramState:
        draw guest or camera-off placeholder using selected deterministic layout
    otherwise draw host-only program
    schedule using the selected visible/worker/frame pipeline
    close transferred VideoFrames and bound queue depth; never retain unbounded frames

conversation routing:
    host return = guest voice, excluding host mic
    guest return = host voice, excluding guest mic
    never route the delayed buyer player or its audio into either return/program
```

Do not use two independent capture calls for the same host mic merely because the call and publisher are separate components. The outgoing publisher accepts `outgoing`; it does not capture devices itself. Program dimensions do not change when CSS/PiP is resized.

## Admission/removal and races (R013–R021, R035, R044)

```text
on trusted Admit(command):
    verify origin/source/schema/capability/event/session/ownerEpoch
    reject old request sequence, wrong guest generation, revoked lease or non-ready guest
    require output publishing; otherwise keep guest backstage with explanation
    service serializes command with expected program revision
    atomically commit next revision to compositor and public audio gate
    acknowledge applied revision to host and guest
    guest shows On air only after acknowledgement

on trusted Remove(command), guest Leave, or detected contribution loss:
    atomically close guest public audio/video gates first
    invalidate that guest generation and pending old admission commands
    commit host-only program revision
    revoke/disconnect guest lease/contribution as appropriate
    acknowledge actual state; keep original host publisher running

on reconnect:
    obtain current valid lease and new connection generation
    recheck usable tracks/transport
    return backstage; never inherit old admitted=true
```

## Output adapter (R025–R029, R037)

```text
on Start publishing click:
    validate live owner and event eligibility
    authorize and resolve current WHIP endpoint/config for this event
    if no supported WHIP configuration:
        show fault; do not guess from RTMP, SRT, legacy URL or copied UI text
    negotiate output using outgoing composed stream
    retain WHIP session resource in memory
    track sender media progress separately from independent audience confirmation
    do not invoke the platform's Start Event automatically

on expired auth / endpoint update:
    invalidate old configuration and resource as appropriate
    resolve fresh authorized config for the SAME event
    retry at 1, 2, 4 seconds plus <=20% jitter, max three automatic retries
    after budget: stable actionable fault; manual Retry requires authorization again

on Stop publishing:
    stop output adapter and DELETE session resource when applicable
    leave event lifecycle to existing host application controls
on event-ended detection:
    reject new joins/admission; close output and notify guest within required budget
```

## Float / return without restarting media (R031–R034)

```text
on Float studio click in studio top-level window:
    if API unavailable/denied:
        retain normal studio, show fallback guidance
        return
    pip = await documentPictureInPicture.requestWindow(requested compact size)
    mount lightweight controls and preview/render surface using same session
    keep engine iframe in original document; do not move/recreate it
    if render surface changes window:
        explicitly move renderer scheduling to a valid visible owner
        preserve canvas/source stream identity or use a verified equivalent pipeline
    on pip.pagehide or Return studio:
        restore controls/render surface and focus to ordinary studio
        do not call final session cleanup
```

This cannot be implemented by blindly portaling an entire iframe-containing React tree. The actual technique is accepted only after independent decoded-program continuity tests. Browser-generated close/unload can be abrupt; combine best-effort local restoration with explicit owner/lease handling.

## Final session disposal (R034, R052)

```text
disposeOwnedSession(reason):
    if already ending/ended: return previous result
    mark ending; close public guest gates
    reject future commands for this owner epoch
    notify guest; cancel retries
    stop publisher; attempt WHIP DELETE
    stop tracks owned by this session, close audio context, workers and render callbacks
    close engine connections; detach listeners/channels
    release owner lease; clear in-memory credentials
    mark ended; export redacted diagnostics

on crash / process termination:
    local cleanup is best effort, not guaranteed
    trusted owner lease expires within 10 seconds
    guests/control clients observe invalidated ownership and cannot resurrect it
```

## Testing boundary

Diagnostics may expose only read-only snapshots. Do not add `forceAdmit`, `setConnected`, simulated successful receiver counters or test-only authorization bypasses. Use controlled devices, a real contribution path and independent receiver artifacts instead. See [acceptance scenarios](acceptance-tests.md).


## Public scope and references

This is a proposed engineering contract, not an approved product specification or a claim about a deployed system. Internal source maps, source revisions, private research, service locations and run artifacts are intentionally not distributed. See [public studio research](../notes/studio-and-popout.md), [integration responsibilities](integration-map.md), and [open review findings](review-findings.md).

Return to [package overview](README.md).
