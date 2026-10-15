# Ten collaboration use cases

## The independent decisions

“Multi-host” can describe several different products. Decide each axis explicitly:

| Axis | Choices |
|---|---|
| Participation | Guest, peer seller, product camera, producer |
| Presentation | One composed program, separate video feeds, linked event pages |
| Audience | Existing audience, partner discovery, shared destination, follower notifications |
| Commerce | One seller of record, alternating sellers, parallel auctions |
| Controls | Invitation, admission, layouts, publishing, listing management, moderation |

Side-by-side video does not require either a particular transport or shared commerce authority. Likewise, combining video does not merge audiences or establish order ownership.

## 1. Invite an expert

An authenticator, artist, or guest contributes conversation and expertise. The original seller owns every item and order.

- **Host:** visible invitation beside the preview; compact admit/mute/remove controls.
- **Guest:** mobile-friendly join link, device setup, backstage state, clear on-air status, and leave control.
- **Buyer:** host and guest visible together; one seller and item context.
- **First question:** is browser participation sufficient, or does the experiment need native app integration?

## 2. Two sellers, one stage

Two sellers collaborate while one item is active at a time. The proposed buyer card identifies its seller explicitly.

- **Host controls:** invitation and turn-taking; inventory remains associated with its owner.
- **Buyer:** both presenters visible; the active item changes with the selling turn.
- **Commerce:** seller switching needs permission and order-attribution support. A video call cannot supply it.
- **Reduced experiment:** keep all items under one host account and clearly state that cross-account selling is unproven.

## 3. Pack battle

Two sellers open collectible packs in a shared presentation. A battle might use alternating rounds or two simultaneous selling lanes.

- **Seller controls:** coordinate rounds while preserving each seller's auction authority.
- **Buyer:** distinguish each side's item, seller, bid action, and checkout.
- **Commerce:** parallel bidding is a separate requirement from a decorative score or shared video.
- **First question:** do buyers need simultaneous auctions, or is alternating presentation enough?

## 4. Link two broadcasts

Two independent events collaborate while retaining their own identities, catalogs, and orders.

- **Host controls:** request and accept an event pairing.
- **Buyer:** dual-player page, combined program, or partner preview with an explicit switch.
- **Audience:** event linking and follower notifications require explicit product design; neither follows automatically from pairing video.
- **First question:** one shared destination, or two destinations with cross-discovery?

## 5. Mobile host and guest

The actual host broadcasts from a phone while conversing with a remote guest.

- **Host controls:** invite, guest readiness, mute/remove, and layouts near the broadcaster's camera controls.
- **Guest:** browser or native contribution, depending on the experiment.
- **Program:** compose on the host device, in a mobile web publisher, or on a server.
- **First question:** does success require a single native host device? A browser-only demonstration leaves that feasibility question open.

## 6. Remote camera and guest

Three video sources represent two people: the host, a product close-up camera, and a remote guest.

- **Host controls:** separate camera-pairing and guest-invitation links.
- **Program:** large product view with smaller host/guest tiles, or selected scene layouts.
- **Audio:** the product camera is muted in the illustrated concept; define one conversational microphone per person.
- **Identity:** a second device does not imply a second seller account.

## 7. Backstage producer

An off-camera collaborator helps run the show through cues or explicitly delegated controls.

- **Producer:** a separate control view; optional private talkback.
- **Permissions:** production layout commands, guest admission, and seller operations are distinct scopes.
- **Buyer:** the producer does not need to appear in the program.
- **First question:** spoken coordination, production-only control, or seller-account delegation?

A media-room invitation must not silently grant access to inventory, orders, moderation, or broadcasting credentials.

## 8. Multi-operator console

Multiple signed-in teammates help run one seller's event without contributing video or joining a media room. This is an operational workspace: a listing runner can manage the queue while a moderator handles chat and another permitted operator manages event actions.

- **Host entry:** an operator invitation or Open operator controls action in the host console.
- **Popout:** listing queue and pin/unpin actions, chat replies and pinned messages, moderation, plus event actions allowed by the operator's role.
- **Team coordination:** presence, who last changed an item, command acknowledgement, and an activity log.
- **Permissions:** listings, chat, moderation, auctions, and ending an event are distinct capabilities. A proposed role assignment is not a claim of existing product support.
- **Commerce:** the original seller remains the seller of record; teammates do not acquire inventory or order ownership.
- **Media:** the broadcaster runs independently. No camera, guest video, media mixing, or P2P media transport is required for this use case.
- **First question:** is the smallest useful experiment a detached control panel or synchronized full-console sessions?

The example assigns Sam to listings and Riley to moderation, with high-impact event actions reserved for a permitted lead or owner. Those names and role boundaries are illustrative design choices.

## 9. Designed co-host journey

A concrete desktop-host/mobile-guest journey reconstructed from the supplied design handoff and sampled demo visuals. Host console entry, invitation, checks, private backstage chat, admission, stacked/side-by-side/PiP layouts, and removal. The seller retains commerce authority. The interactive preview is a simulation, not a connected call.

Three routes: native guest plus program mixer; mobile web guest plus browser mixer as an explicit feasibility shortcut; browser conversation plus OBS output. See [design handoff](design-handoff.md).

## 10. Bring a viewer on stage

A proposed extension for a collector, previous buyer, or winner to join briefly. The supplied research discusses community participation separately from the initial guest flow. The explorer compares host-selected invitation, a proposed viewer request queue, and a planned guest moment. All retain checks, backstage, host admission/removal, and the original seller's item context.

Identity, consent, eligibility, reporting, spam limits, and revocation need product and engineering decisions. A viewer request queue is an alternative proposed by this study, not an established handoff feature.
