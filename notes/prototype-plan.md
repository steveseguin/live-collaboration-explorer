# Choosing a first prototype

A prototype can be web, native, or server-based. Its scope should follow the uncertainty it is meant to resolve.

## Candidate experiments

| Question | Useful experiment | What it would leave open |
|---|---|---|
| Can a host invite and comfortably converse with a guest? | Two-person browser room with backstage/admit/remove states | Native app integration, audience growth, and commerce |
| Does the invitation fit beside existing host controls? | Console entry plus a separate companion room | Actual media publication and app lifecycle |
| Can the combined program reach a compatible live event? | Browser composition → WHIP test receiver → buyer playback | Production authorization, reliability, and mobile performance |
| Can a native host do this on one phone? | One-platform app spike: receive, compose, converse, publish | Cross-platform behavior and full seller workflows |
| Do buyers understand two seller contexts? | Paired buyer mockup with explicit seller labels and item switching | Real cross-account permissions and orders |
| Does a pack battle require simultaneous auctions? | Compare alternating rounds with two independent item lanes | Auction/backend integration and fulfillment |
| Can an off-air producer help safely? | Production-only remote control or private talkback | Seller-account delegation unless separately implemented |
| Can teammates run one show without any video collaboration? | Operator popout with listing queue, chat, moderation, scoped event controls, and synchronized state | Real account delegation and backend permissions unless actually integrated |

## A narrow media prototype

Proposed scope:

1. Host creates a room and copies a guest link.
2. Guest selects devices and joins backstage.
3. Host and guest converse, with clear private/on-air status.
4. Host admits the guest into a simple two-person program layout.
5. A compatible test ingest receives the combined program.
6. Guest departure returns the program to the host.

Possible technical foundation: [VDO.Ninja SDK](https://github.com/steveseguin/ninjasdk) for conversation/contribution, with a separate compositor and publishing adapter.

## A narrow native spike

If native hosting is the actual objective, focus on one platform and a small demonstration:

- Receive a remote participant while capturing the host.
- Produce video frames containing both participants.
- Maintain conversational audio and a correct outgoing mix.
- Publish to a compatible test receiver.
- Observe device load, audio routing, disconnects, and app foreground/background behavior.

This is a prototype even if it uses native code. A visual native screen alone does not establish that the media path works.

## A narrow operator prototype

Show the host opening a separate operator page, with two illustrative teammate roles. Include the listing queue, pin/unpin state, chat replies, moderation actions, and role-limited event controls. Show the actor and acknowledgement for each action.

A UI-only prototype can explore placement and workflow with simulated state. An integrated spike should demonstrate individual sign-in, backend permission checks, shared event updates, stale-command rejection, and an auditable action trail. Neither version needs a guest call or video compositor. A second device is another useful target for the same operator page.

## Separate follow-up decisions

Audience discovery and follower notifications; shared-event identity; seller switching; simultaneous auction lanes; guest eligibility; scoped permissions; order attribution; moderation; and production reliability.

These should not be treated as implicitly solved by a successful media demonstration.

## Starting from the supplied design

The [designed co-host journey](design-handoff.md) supplies a concrete UX reference for the narrow media prototype above. Start with desktop console controls and one mobile guest. Decide whether mobile web is an explicit shortcut or a native guest is required. Keep community selection and co-selling separate from media feasibility. The interactive website illustrates lifecycle and layout choices but does not connect media or validate device behavior.
