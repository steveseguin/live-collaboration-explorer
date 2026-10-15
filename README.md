# Together on Live

A visual exploration of live-commerce collaboration: **eight use cases, three implementation options each**.

**[Browse the website](https://steveseguin.github.io/live-collaboration-explorer/)**

Switch between host controls, the participant call or operator popout, and the buyer view. Select an implementation to see its connection diagram, proposed placement, and tradeoffs. Use **Compare scenarios** for the audience and commerce overview.

This is an unofficial design study by Steve Seguin. All interfaces, participants, listings, and prices are illustrative. The scenarios are proposals, not statements about existing eBay capabilities or a product roadmap.

## Scenarios

1. Invite an expert — one host, one guest, one seller of record.
2. Two sellers, one stage — share the presentation and alternate items.
3. Pack battle — compare two sellers with potentially parallel commerce.
4. Link two broadcasts — preserve each event's identity.
5. Mobile host and guest — compose a program from a phone.
6. Remote camera and guest — combine a product close-up and conversation.
7. Backstage producer — coordinate off camera with explicit permissions.
8. Multi-operator console — share listings, chat, moderation, and permitted event actions without video.

## Notes

- [Use cases](notes/use-cases.md) — participants, audience, commerce, and placement.
- [Implementation options](notes/implementation-options.md) — 24 possible routes and their tradeoffs.
- [Prototype plan](notes/prototype-plan.md) — questions and experiments that could guide a first build.
- [Sources and assumptions](notes/sources-and-assumptions.md) — public references and boundaries.

## Run locally

```sh
python -m http.server 8767 --bind 127.0.0.1
```

Open `http://127.0.0.1:8767/`. No install or build step is required. Google Fonts is optional; local system fonts are the fallback.

## Files

- `index.html` — website shell and notes dialog.
- `app.js` — scenario content, previews, and interactions.
- `styles.css` — responsive interface styling.
- `operators.js` / `operators.css` — control-only scenario and operator-workspace mockups.
- `assets/` — original SVG illustrations.
- `notes/` — Markdown design notes.
- `.nojekyll` — direct static publishing with GitHub Pages.

GitHub Pages serves the root of the `main` branch. Updates to these files publish through Pages.

The website has no broadcasting implementation, camera/microphone access, login, checkout, analytics, or SDK dependency. A possible future transport is the [VDO.Ninja SDK](https://github.com/steveseguin/ninjasdk).
