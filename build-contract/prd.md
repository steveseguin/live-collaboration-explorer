# PRD — browser co-host prototype

## Goal

Demonstrate a complete guest-video flow in the context of the existing host console: invite a mobile browser guest, prepare devices, coordinate backstage, admit the guest into a mixed program, operate the show, and remove/leave without interrupting the host. The implementing AI must prove actual media delivery and lifecycle behavior, not just recreate the concept explorer.

## Personas and authority

| Participant | Required experience | Authority |
|---|---|---|
| Original seller / authorized host | Console entry, persistent studio, guest readiness, admission/removal, layouts, capture/output controls | Event-scoped host authority verified through a trusted service |
| Invited guest | Mobile-friendly browser invite, consent, device checks, private conversation, clear backstage/on-air state, self controls and leave | Contribution to one session only; no seller, moderation, inventory, order or ingest authority |
| Buyer | Original show and commerce context; host plus admitted guest in one program | Existing buyer behavior; this prototype does not change bidding/orders |

## Scope selected for this contract

- One desktop host using Chrome or Edge; one physical Android Chrome or iPhone Safari guest.
- Existing console keeps listings, public chat and event controls. A compact co-host entry opens/focuses a persistent studio window.
- The studio owns a VDO.Ninja engine iframe, host/guest conversation, a custom 720x1280 canvas, an outgoing audio bus and WHIP publication.
- Float the studio's controls/preview/render surface with Document PiP where supported. Keep the live iframe fixed; fall back to the ordinary studio window.
- Three program layouts: Stacked, Side by side, Picture in picture. These are broadcast layouts, distinct from browser Document PiP.
- Private text backstage. Spoken private host talkback is deferred because host audio may already be public; normal conversational audio and public program audio still require deliberate routing.
- Consent, access, single-guest capacity, revocation, reconnect behavior and truthful fault states are part of the prototype.

The normative detail and mappings are in [requirements.md](requirements.md) / [contract.json](contract.json). Numeric thresholds are proposed engineering defaults, recorded in [decisions](decisions-and-assumptions.md).

## Host journey

1. Open an eligible event; enable the prototype only through the prepared environment's feature configuration and authorization.
2. Select **Open co-host studio**. Repeated selection focuses the same event/session owner. Blocked popups produce actionable guidance and no hidden capture.
3. In the studio, select **Prepare host**, grant camera/microphone access and choose devices. No device access begins just by loading the console/studio.
4. Create a guest-only invitation. Copy or share through the available system interaction. Sending email/push notifications is not a required delivery integration.
5. Observe guest setup and backstage readiness. Use clearly private text communication while retaining public buyer chat visibility in the console.
6. Start the program publisher separately from the platform event lifecycle. Existing Start/End Event and seller-consent controls remain authoritative.
7. Select **Bring guest on air** after guest readiness and publisher readiness. Apply an admission revision, gate both video and audio, and acknowledge the actual program state to the guest.
8. Change layout, mute/exclude guest media, use listings/chat, and optionally float/return the studio while the same session continues.
9. Remove the guest or accept guest departure. Program returns to the host; a replacement needs a new valid lease and admission.
10. Stop publishing separately from ending the event. On final studio stop, release all owned resources. Detect an ended event and tear down its output.

## Guest journey

1. Open an event/session-bound invitation and see the original host/event identity and participation explanation.
2. Explicitly select **Check devices**; grant or recover camera/microphone permission. A direct-open option is available if the embedding context blocks capture.
3. Actual usable tracks and transport readiness enable **Join backstage**. Permission granted or iframe loaded alone is not readiness.
4. Wait backstage with host preview/private conversation; the guest is excluded from the public program.
5. Receive an acknowledgement of host admission and a clear **On air** state. This means inclusion in the outgoing program; it is not proof that the platform event is publicly live or that every delayed buyer has received it.
6. Use self camera/mic controls or **Leave show**. If capture/connection is interrupted, return through readiness/backstage rather than automatically returning on air.

## Required failures and transitions

Invitation expired/revoked/reused; second guest; declined invitation; popup blocked; denied/dismissed/busy/missing devices; unsupported browser/canvas; iframe permission failure; guest loss and replacement; host device loss; output/authorization failure; endpoint change; console navigation/reload; PiP return/browser-close; studio final stop/crash; event ended; stale or forged commands. Each has an acceptance scenario and a truthful, recoverable UI state.

## Explicit non-goals

Native-app guest integration; mobile hosting; more than one guest; co-selling or shared seller inventory; simultaneous auctions or pack-battle commerce; linked event audiences; community request queues; multi-operator permissions; recording as a product feature; a general scene/graphics/production suite; automated email/push delivery; production rollout, business approval or a committed product roadmap.

Using stock VDO.Ninja mixer/scene output is a useful first media experiment. Full acceptance of **this** contract requires the requested custom canvas/audio program and must not silently substitute screen sharing or OBS.

## Success and acceptance

The full flow works on the specified desktop hosts and real guest phones, reaches independent receiver and actual QA buyer playback, preserves the existing seller context, meets measured thresholds, and passes all 80 required test variants. The [completion ledger](evidence-and-completion.md) is the definition of done. A laboratory-only result must be labeled laboratory-only.


## Public scope and references

This is a proposed engineering contract, not an approved product specification or a claim about a deployed system. Internal source maps, source revisions, private research, service locations and run artifacts are intentionally not distributed. See [public studio research](../notes/studio-and-popout.md), [integration responsibilities](integration-map.md), and [open review findings](review-findings.md).

Return to [package overview](README.md).
