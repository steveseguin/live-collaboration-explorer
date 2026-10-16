# Persistent browser studio and popout research

October 2026 public technical notes for a proposed desktop-host/mobile-browser-guest prototype. These are source-backed integration ideas, not a working call, measured benchmark, platform API claim or production approval.

## Selected direction

Keep a compact launcher/status panel beside the selling console. A separate ordinary studio window owns the media engine, custom compositor, audio graph and publisher. Offer Document Picture-in-Picture (Document PiP) as an optional floating view of that same session.

The console can reload or navigate without intentionally owning capture cleanup. The ordinary studio is the independent lifetime boundary; Document PiP is still tied to its opener.

## Engine reuse versus custom composition

| Route | Reused behavior | Still requires proof |
|---|---|---|
| Stock VDO.Ninja mixer/scene output | Contribution, conversation, director controls, scene/output workflows | Actual ingest compatibility, consent, public/private routing and deployment |
| Same-origin engine plus custom studio | Existing iframe engine and explicit permitted decoded media access | Stable adapter, custom canvas/audio output, exact origin policy and lifecycle |
| Cross-origin media bridge | Hosted engine with explicit frame/audio forwarding | Supported API/browser behavior, throughput, backpressure, audio and cleanup |

The [VDO.Ninja mixer source](https://github.com/steveseguin/vdo.ninja/blob/develop/mixer.html) and [iframe guide](https://docs.vdo.ninja/guides/iframe-api-documentation) are useful starting points. Pin the engine/build used by an implementation; moving development URLs are references, not reproducible deployment pins.

A parent's iframe controls do not grant access to cross-origin video DOM or streams. Sibling subdomains are not the same origin. An explicit documented bridge is a different integration route, not an automatic exemption from browser policy.

The [director API](https://docs.vdo.ninja/guides/iframe-api-documentation/iframe-api-for-directors) provides media-room controls. Director authority does not confer seller, moderation, commerce or ingest authority in another application.

## Public program versus conversation

A custom program needs a fixed-size canvas video track and an explicit audio bus. Keep guest video **and audio** outside the public program until acknowledged host admission. Host/guest conversational return excludes each participant's own microphone and delayed buyer playback.

Initial private cues are text. Spoken host talkback is not automatically private while the host mic is already in the public program. Do not duplicate host microphone capture just because conversation and publication are separate modules.

The publishing adapter must accept the composed MediaStream rather than silently capturing its own camera. [WHIP, RFC 9725](https://www.rfc-editor.org/rfc/rfc9725.html), defines protocol behavior; endpoint authorization, codecs, ICE, CORS and real receiver delivery still need deployment evidence.

## Floating controls without moving the engine

[Document PiP](https://developer.chrome.com/docs/web-platform/document-picture-in-picture) can display HTML controls and media. Request it from a top-level user gesture, feature-detect support, and retain an ordinary-window fallback.

Do not blindly portal an iframe-containing UI between documents. Keep the engine fixed and use a lightweight floating control/preview/render view, unless a different approach is demonstrated to preserve the live session.

An existing connection does not prove fresh composed frames. [Animation callbacks](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) and [background timers](https://developer.chrome.com/blog/timer-throttling-in-chrome-88) can behave differently in hidden documents. Measure decoded receiver frames and source motion through focus changes, float/return, PiP close and console reload.

Additional references:

- [Document PiP specification](https://wicg.github.io/document-picture-in-picture/)
- [Document PiP requestWindow](https://developer.mozilla.org/en-US/docs/Web/API/DocumentPictureInPicture/requestWindow)
- [Embedded iframe lifecycle discussion](https://github.com/WICG/document-picture-in-picture/issues/97)
- [State-preserving moveBefore constraints](https://developer.mozilla.org/en-US/docs/Web/API/Element/moveBefore)
- [Playwright fixtures](https://playwright.dev/docs/test-fixtures) and [configuration](https://playwright.dev/docs/test-configuration)

## Build package and remaining risks

The [build contract](../build-contract/README.md) expands this direction into PRD/TRD, pseudocode, 60 requirements, 40 scenarios and 80 mandatory variants. It includes eight browser cases and assisted media, device, networking, PiP, performance and QA procedures.

It is still **specified, not implemented or accepted**. The [open review findings](../build-contract/review-findings.md) cover evidence provenance, independent measurements, owner-expiry fencing, and testing reload while publishing. Those findings have not been fixed by publication.

Return to [design notes](README.md) or the [repository overview](../README.md).
