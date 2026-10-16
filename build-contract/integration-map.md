# Integration responsibilities

This public map describes proposed seams, not a private application's source layout or existing APIs. A builder must map each responsibility to the actual authorized checkout and record the decisions in a private build manifest.

| Surface | Required behavior | Proposed boundary |
|---|---|---|
| Selling console | Listings, buyer chat and event controls remain usable; reload/navigation must not own or destroy the media session | Small launcher and truthful session-status adapter |
| Studio page | Independent event-bound lifetime, explicit capture, one engine/compositor/audio graph/publisher | Authenticated top-level application window |
| Host authority | Verify account/event eligibility at a trusted boundary; default the feature off | Server-side authorization and scoped host capability |
| Guest invitation | Event/session-bound, expiring, atomic single redemption and revocation | Trusted invite and guest-lease service |
| Session ownership | Exclusive owner lease across browsers, not only a named popup/localStorage lock | Trusted service plus publish-session enforcement; see the open fencing issue |
| Media engine | Pin the VDO.Ninja build; validate origin/source; explicitly obtain permitted tracks or frames | Stable iframe and documented media adapter |
| Program | Fixed 720x1280 canvas and explicitly gated public audio bus | Compositor and separate conversational/program routing |
| Ingest | Accept the composed MediaStream; resolve current event-authorized WHIP config | Isolated publisher/authorization adapter |
| Endpoint changes | Invalidate obsolete credentials/resources and recover with bounded retries | Event-scoped configuration invalidation |
| Event lifecycle | Existing consent and Start/End remain authoritative and separate from publishing | Read canonical event state; stop output when the event ends |
| Floating view | Same session; never reparent a live engine iframe into PiP | Lightweight controls/preview/render host with ordinary-window fallback |
| Guest page | Explicit consent/checks, backstage/on-air truth, self controls and leave | Guest-only capability; no seller or ingest authority |
| Existing commerce messages | Preserve the application's approved message bus and authorization | Separate studio/engine protocol; no raw top-window commerce commands |
| Diagnostics | Opt-in, redacted, read-only snapshots correlated with independent evidence | No force-admit, fake-ready or authorization bypass |

## Decisions required before integration

Choose actual routes and feature/permission mappings; exact studio/engine/guest origins; deployment/CSP/Permissions-Policy; media-access API; owner renewal and publish-session fencing; guest identity policy; WHIP endpoint/auth/codec/ICE/CORS/resource contract; independent receiver; physical device matrix; and prepared non-production buyer access.

No local source path, backend operation, permission name or current deployment is implied by this map. Local test services can establish laboratory behavior, not real platform authorization.

See [TRD](trd.md), [implementation milestones](implementation-plan.md), [open review findings](review-findings.md), and [package overview](README.md).
