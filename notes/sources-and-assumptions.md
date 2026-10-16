# Sources and assumptions

## Scope and provenance

This repository contains Steve Seguin's illustrative scenario analysis and proposed implementation options. The interactive screens and architecture diagrams are original mockups. Two selected earlier source flow diagrams are included separately in [sources/](../sources/README.md). All participant names, listings, prices, bids, connection states, and scores are fictional.

The public notes make no claim about private product plans, current native implementation interfaces, actual deployment state, or authorized access to a live-commerce system. Selected flow images and a summary of a maintainer-supplied design handoff are included. Full originals, research participant details, access information, internal source links, conversations, and test-environment details are excluded from the public repository. See the [design handoff note](design-handoff.md) for the distinction between observed UX and proposed implementation routes.

## Public technical references

- [VDO.Ninja SDK repository](https://github.com/steveseguin/ninjasdk) — possible transport for media and data.
- [SDK website](https://sdk.vdo.ninja/) — examples and feature overview.
- [Connection guide](https://sdk.vdo.ninja/docs/connecting.html) — media publishing/viewing, room interoperability, and TURN considerations.
- [Integration guide](https://sdk.vdo.ninja/docs/guides.html) — distinction between SDK transport and application responsibilities.
- [Studio and popout research](studio-and-popout.md) — VDO.Ninja iframe/director references, exact-origin media access, browser PiP/lifecycle references, WHIP and Playwright.

The [public build contract](../build-contract/README.md) contains proposed architecture and authored acceptance tooling. Its generic integration map does not disclose private source structure or claim existing backend APIs. Private research attachments, source maps, service locations and run evidence remain excluded.

The site does not install or load the SDK. SDK compatibility with any particular broadcasting platform, browser, native application, or ingest endpoint is unverified here.

## Assumptions to validate

- A guest contributes audio/video without receiving seller privileges.
- A seller collaboration may need either one shared event or two linked events.
- Audience discovery requires its own product and backend design.
- Orders should identify the relevant seller under any shared-selling model.
- A single composed program and multiple viewer-rendered feeds are both possible architectural directions; neither is selected as a universal answer.
- Native publishing needs a supported media-input seam, not simply a browser overlay.
- Transport messages must be authorized independently of peer connectivity.
- Device performance, audio behavior, browser support, endpoint authentication, and reconnect handling require practical investigation.

Written October 2026. This is an unofficial concept exploration, not an eBay product announcement.
