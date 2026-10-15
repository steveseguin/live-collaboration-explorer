# Design handoff: guest participation

## What was supplied

A design handoff document, a roughly ten-minute intern demo recording, a Figma research archive, and a photograph of chat controls. This summary records selected product behavior; it is not a claim of engineering completion or a launch commitment.

The public repository includes two selected earlier flow diagrams. Full originals are copied into the ignored `sources/local-originals/` folder in the maintainer's local checkout. They are not published by GitHub Pages. See the [source inventory](../sources/README.md).

## Two additions to the explorer

### Designed co-host journey

[Open the interactive reconstruction](https://steveseguin.github.io/live-collaboration-explorer/#cohost).

The demonstrated pairing is a **desktop host and a mobile guest**:

1. Host copies/sends an invitation from a compact co-host module.
2. Guest follows the invitation and checks network, camera, and microphone.
3. Guest waits backstage; host sees readiness/preview and can communicate privately.
4. Host admits the guest into one public program.
5. Host chooses stacked, side-by-side, or picture-in-picture presentation.
6. Removal ends guest participation and returns the program to the host.

Buyer chat remains visible below the guest module. The original seller keeps the commerce context. Appearing on camera does not establish moderation, inventory, order, or account authority.

Implementation proposals:

| Route | Placement | Main uncertainty |
|---|---|---|
| Native guest + program mixer | Desktop console controls, guest app, browser or server compositor | Native contribution, conversational return, identity and app lifecycle |
| Mobile web + browser mixer | Console invitation, separate host room, phone-friendly guest page | Explicit native-UX shortcut; mobile audio and publishing feasibility |
| Web conversation + OBS | Browser call, clean media source, OBS scene and existing ingest | Correct audio routing; demonstrates desktop production rather than native integration |

The SDK can provide contribution/conversation transport. It does not choose the compositor, grant seller permissions, or connect event authorization automatically.

### Bring a viewer on stage

[Open the proposed extension](https://steveseguin.github.io/live-collaboration-explorer/#community).

The supplied material explores community participation, including collectors, previous buyers, or winners. It is presented separately from the initial expert-guest flow. The explorer offers three **proposals**: host-selected viewer invitation, a viewer request queue, and a planned guest segment. The request queue is an alternative proposed here, not a demonstrated handoff requirement.

All routes need consent, identity binding, eligibility, reporting/removal, and clear private/on-air states. A buyer guest does not become a second seller. The site reuses the same lifecycle to make that distinction visible.

## Source versions and limits

- The supplied archive represents a research file. The DOCX links a **separate final design/prototype file**. Do not treat the archive as a complete export of that final design.
- Earlier flow variants disagree about desktop/mobile support, guest capacity, timing, and some guest capabilities. The two published images retain their draft labels and assumptions; they are background evidence, not an approved specification.
- The later demo visibly presents desktop host controls, mobile guest setup, private backstage chat, and three layouts. Community expansion and remote co-selling appear as later directions in that presentation; they are not shipping commitments.
- The handoff still calls for design-system, placement, icon, wording, and review work. A completed design handoff does not establish completed engineering.
- The recording was reviewed through sampled visuals and selected full-resolution slides, not audio transcription. The interactive Figma prototype and media implementation were not exercised.
- The chat photograph shows reply, highlight, delete, and mute actions. It does not prove delegated multi-operator access. That remains a separate concept.

## Proposed bounded build

`invite → guest checks → backstage → host admission → combined buyer program → removal`

Choose the target explicitly: browser feasibility shortcut, native guest integration, or native host composition. A one-platform native spike is still a prototype when scoped to these questions. Investigate backstage isolation, conversational audio, outgoing mix, authentication, reconnects, and device load.

## Provenance

Supplied October 15, 2026 by the repository maintainer: `Aubrey Cantrell _ Deliverables & Handoff.docx`, `Aubrey Cantrell intern demo .mp4`, `Multi-Host-Streaming-Archive.zip` and its extracted flow screenshots, and `IMG_1017.heic`. Attribution to the original design team is retained; no new license is granted for the selected source diagrams. Internal links, participant research details, raw recordings, and account/access information are excluded from this public summary.

Return to [all notes](README.md).
