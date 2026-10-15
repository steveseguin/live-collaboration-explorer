# Implementation options

All options below are proposals. Nothing in this list establishes current platform support, endpoint availability, or implementation effort estimates.

## Guest expert

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Browser companion + WHIP | Console invitation; separate conversation/composition page; compatible test ingest | Validates the experience; browser performance and ingest authentication remain open |
| OBS guest source | Browser conversation; clean source or scene in OBS | Useful desktop baseline; does not prove native host integration |
| Native guest + host mixer | Guest app contribution; host-side browser or server mixing | Requires native media contribution and return conversation |

## Two sellers, one stage

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Mixed program + active seller | Mixer plus shared-event commerce state | Consistent buyer video; seller switching needs backend authority |
| Two feeds + shared event | Independent publishers; dual-feed buyer renderer | Flexible layouts; playback synchronization and commerce still need design |
| Host-owned inventory | Companion call and existing single-seller catalog | Smaller experiment; does not validate both sellers' own orders |

## Pack battle

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Pair existing events | Two original auctions; new paired viewer | Preserves event ownership; dual playback and purchase UX need work |
| Shared battle event | Two auction lanes in a new shared session | Deepest integration across auctions, bidding, risk checks, and checkout |
| Alternating rounds | Shared presentation; one active seller/item | Tests battle appeal without simultaneous auctions; attribution remains necessary |

## Linked broadcasts

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Dual-player page | Buyer renders both event feeds | No required video mix; define audio, active commerce, and discovery |
| Third combined program | Server receives both source feeds and publishes another program | Adds operations, latency, and another program identity |
| Partner preview + handoff | Original event page links to the partner event | Lighter viewing model; not full simultaneous side-by-side presentation |

## Mobile host + guest

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Native composition | Host app receives guest media, mixes, and publishes | Must prove audio ownership, frame composition, thermals, and lifecycle |
| Mobile web publisher | A browser replaces the app publisher for the experiment | Can explore the flow without app changes; does not prove the app path |
| Server composition | Compatible host/guest contributions; server mixer and audio return | Reduces on-device composition; still needs contribution and session integration |

## Remote camera + guest

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Desktop web mixer | Receives product camera and guest alongside host | Multiple video sources increase bandwidth and composition work |
| OBS source collection | Browser call plus separate camera/guest sources in OBS | Familiar production approach; external tool setup remains |
| Native camera hub | Host app receives camera and guest and composes locally | More concurrent media work than a simple two-person call |

## Backstage producer

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Authorized console access | Approved seller-delegation mechanism and backend checks | Verify which actions can actually be delegated |
| Production-only remote | Scoped commands to a paired broadcaster | A data channel is transport; the receiver must authorize every command |
| Private talkback | Producer sends audio cues to host | Validates coordination, not remote operations; keep audio out of public program |

## Multi-operator console

| Route | Where it runs | Main tradeoff |
|---|---|---|
| Shared host console | Multiple individually authorized sessions for one seller event | Reuses the console; needs synchronized state, action-level permissions, and concurrent-change handling |
| Operator popout | A compact separate page for listings, chat, moderation, and permitted event actions | Focused UI; still requires backend authorization, reconnect handling, acknowledgements, and stale-action protection |
| Role-specific desks | Dedicated listing, moderation, and event-lead workspaces | More tailored workflows; more surfaces and explicit role/handoff design |

This is a control-only architecture. Operators send authenticated commands to event services and receive shared state updates. Transport does not grant authority. Audit actor identity, enforce roles at the backend, and define how conflicting actions are rejected or resolved. A copied popout URL alone must not grant seller access.

## Common media boundaries

- Participants need a conversational audio path, independent of delayed public playback.
- The program mix needs all intended public voices; each participant's return audio should exclude their own microphone.
- Avoid duplicating host audio through both a guest source and another capture path.
- Explicitly separate backstage media from public output.
- P2P can reduce central media processing; signaling, TURN, and connection recovery still exist.
- A mixer cannot resolve item ownership, follower notifications, or permission enforcement.
- A viewer that renders multiple streams needs an audio policy and a strategy for timing differences.

## Designed co-host journey

| Route | Placement | Tradeoff |
|---|---|---|
| Native guest + program mixer | Guest app, compact desktop console panel, browser/server compositor | Closest to the demonstrated guest UX; native contribution and conversation integration required |
| Mobile web + browser mixer | Phone-friendly guest page plus separate host room | Feasibility shortcut; does not implement a native guest target |
| Web conversation + OBS | Browser talkback and clean media source, composed OBS output | Useful desktop media demonstration; audio routing and external setup remain |

## Bring a viewer on stage

| Route | Placement | Tradeoff |
|---|---|---|
| Host invites a viewer | Private invitation from host chat action | Requires identity binding, consent, eligibility, and removal |
| Viewer requests to join | Buyer request action and host queue | Proposed alternative; adds spam controls and queue privacy |
| Arrange a guest moment | Pre-show invite and event-linked setup | Predictable participation; notification failures and missed segments remain |

See [design handoff](design-handoff.md) for observed behavior, draft contradictions, and limits.
