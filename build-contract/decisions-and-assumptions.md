# Decisions, defaults and external dependencies

## How to interpret this file

These decisions make the prototype implementable without silently inventing product approvals. `contract.json` version 1.0.0 is binding for acceptance once used. Changing scope, a threshold or a mandatory variant requires a versioned contract change and invalidates affected evidence. The implementing AI may choose internal techniques that satisfy the contract; it may not self-approve exceptions to acceptance.

## Selected defaults

| Decision | Baseline | Reason / boundary |
|---|---|---|
| Product | Guest video under original seller control | Matches the supplied handoff; broader commerce remains separate |
| Host | Desktop Chrome and Edge; record exact versions/OS/hardware | Bounded first implementation; no assumption that all browsers support Document PiP |
| Guest | Mobile web, physical Android Chrome and iPhone Safari required | Explicit prototype shortcut from native designs; emulation does not prove device capture/audio |
| Studio | Independent event-bound window owns media | Console tab switching/reload must not destroy the producer |
| PiP | Optional capability, mandatory supported-browser/fallback behavior | Top-level, user-gesture invocation; never move a live engine iframe between documents |
| Media engine | Pinned VDO.Ninja iframe deployment | No custom signaling stack; exact same-origin media access preferred for own canvas |
| Program | Custom 720x1280 canvas, 30 fps target, explicit Web Audio bus | Custom canvas is requested; stock scene/tab capture alone is insufficient |
| Guest capacity | One host plus one guest | A second contributor is rejected; replacement is explicit |
| Invitation | Event/session scoped, expires within 15 minutes before redemption, single redemption | After redemption use a separate guest lease; do not force a 15-minute call limit |
| Guest lease | Bounded renewable lease with active owner/generation checks | Reconnect/replacement may not reuse a revoked admission; exact opaque service API is implementation-specific |
| Studio owner lease | At most one owner; lost-owner expiry at most 10 seconds | Prevent duplicate producers and abandoned sessions; trusted control service arbitrates |
| Private cues | Text private chat required; spoken host-only backstage talkback deferred | A host already on air cannot assume speech to guest is private |
| Output retry | Three automatic retries at 1, 2, 4 seconds, up to 20% jitter | Bounded, visible failure; manual retry needs current authorization |
| Removal | Program-ingress exclusion within 1 second | Audience CDN delay is measured separately |
| Guest loss | Detect within 2 seconds, exclude within another 1 second | No indefinite frozen guest; recovery returns backstage |
| Observed mobile suspension | Exclude within 2 seconds of observed platform mute/end/suspension | Platform event latency itself is recorded; do not pretend the app controls the OS |
| Event end | Stop output within 5 seconds of detection | Existing event lifecycle remains authoritative |
| Steady performance | At least 25 decoded fps, no moving-source freeze over 1 second | Controlled declared hardware/network; target is 30 fps |
| Soak | 30 minutes; heap median growth <=100 MiB after warmup | Record queue sizes and active publisher counts; no forced-GC trick to hide leaks |
| Timing | p95 A/V skew <=150 ms; one-way call <=750 ms; local program <=2 seconds | Controlled network, at least 30 observations; this is not a buyer-CDN latency SLA |
| Acceptance | Every case variant and required evidence | No skips, not_run, blocked, partial or mocked-only substitution |

## External dependencies that must be resolved before full acceptance

1. **Trusted authorization/control service:** actual event/host eligibility, invite redemption/revocation, owner lease and command authorization. Proposed operations in the TRD are not existing host application/GraphQL APIs. A local test service can support laboratory validation; it cannot prove real platform authorization.
2. **Current ingest contract:** prepared event with a supported WHIP endpoint, actual authentication semantics, supported codecs, CORS/ICE behavior and session cleanup. A displayed stream URL is not the whole publish authorization contract.
3. **Origin and policy:** actual HTTPS studio/engine/guest origins and camera/microphone permissions/CSP. Do not rely on `document.domain`, sibling domains, a permissive iframe attribute alone, or arbitrary cross-origin DOM access.
4. **Real mobile devices and desktop PiP:** actual physical phones and headed Chrome/Edge. Missing hardware is a blocked result, not a pass.
5. **Direct and relay networking:** a real functioning TURN route with selected candidate evidence. A configured URL or a mocked ICE state is insufficient.
6. **Prepared QA event/buyer access:** test seller, known item and an authorized event. No purchases or real bids are necessary. No publication to production is authorized by this plan.
7. **Independent observation:** a receiver recording/analysis path, synchronized or bounded-uncertainty timing method, and actual QA buyer evidence.

## Integration choices the builder must record

- Exact feature flag and server permission/eligibility mapping. No existing co-host permission API is assumed.
- New route/page/module names and whether the engine is vendored or served by a separately controlled same-origin application.
- How a persistent studio discovers/focuses the current owner after console reload, and how the backend prevents split ownership across browsers/devices.
- How canvas frames continue while windows/frames are hidden or floated. Technique is flexible; measured receiver continuity is mandatory.
- Whether WHIP publication uses a supported VDO.Ninja publishing seam or another isolated adapter. It must accept the composed MediaStream and preserve current event authorization.
- Guest identity/account policy. The baseline requires an event-scoped contribution capability and truthful host/event identity; native account activation/email/push is not silently inferred as implemented.

Record these in the implementation build manifest. Unresolved decisions remain blockers for their mapped cases. Do not mark an integration decision as an observed existing feature merely because its interface is written in pseudocode.


## Public scope and references

This is a proposed engineering contract, not an approved product specification or a claim about a deployed system. Internal source maps, source revisions, private research, service locations and run artifacts are intentionally not distributed. See [public studio research](../notes/studio-and-popout.md), [integration responsibilities](integration-map.md), and [open review findings](review-findings.md).

Return to [package overview](README.md).
