# Browser co-host build and acceptance contract

Build a desktop-host/mobile-browser-guest prototype using a pinned VDO.Ninja iframe, a custom canvas/audio program, and a separate persistent studio. The selling console keeps a compact launcher/status panel instead of owning the media session.

**Status: specified, not implemented or accepted.** The visual explorer is not this product. No product acceptance variant is claimed passed. This is an unofficial proposed engineering contract, not a platform product announcement or an authorization to deploy.

**Read the [open review findings](review-findings.md) before relying on the completion checker.** The current gate has known evidence-validation gaps; a green exit code alone is not sufficient acceptance.

## Package contents

1. [PRD](prd.md): scope, participants, host/guest flows, failure states and non-goals.
2. [Decisions and dependencies](decisions-and-assumptions.md): proposed defaults and external blockers.
3. [Integration responsibilities](integration-map.md): platform-neutral seams a builder must resolve.
4. [TRD](trd.md): media routing, authority, ownership, state machines and cleanup.
5. [Pseudocode](pseudocode.md): implementation guidance, not existing platform APIs.
6. [Implementation plan](implementation-plan.md): milestones and evidence boundaries.
7. [Requirements](requirements.md) and [machine-readable contract](contract.json): 60 requirements mapped to 40 scenarios and 80 mandatory variants.
8. [Acceptance scenarios](acceptance-tests.md): eight supplied browser cases plus assisted media, device, networking, PiP, performance and integration procedures.
9. [Evidence and completion](evidence-and-completion.md): artifact provenance, measurement methods and completion policy.
10. [Validation tooling](validation/README.md): external browser harness, fixture generator, media analyzer, source snapshot and ledger checker.
11. [Review findings](review-findings.md) and [review record](review-record.md): known limitations and publication checks.

## Instructions to a builder

- Work only in an authorized implementation checkout and read its contributor/testing/messaging guidance.
- Resolve real host authorization, guest capabilities, media access, ingest and receiver dependencies before claiming integration.
- Keep capture, device consent, guest admission, publication and event Start/End as separate states.
- Do not lower thresholds, remove variants, fabricate artifacts or substitute app counters for received media.
- Use physical phones for device claims and headed desktop browsers for Document PiP claims.
- Report laboratory-only results, blocked dependencies and unexecuted variants explicitly.
- Fix or otherwise independently account for every open review finding before using this as a full acceptance gate.

## Public distribution

This is a **public-sanitized distribution**. It keeps build specifications, authored validation source and public technical references. It intentionally excludes private source maps/revisions, implementation-source excerpts, internal document/chat links, private service locations, original research attachments, credentials, auth state, generated media and run artifacts.

The public contract has its own SHA-256. Evidence from any other distribution must not be reused as if its contract hash matched. No private snapshot equality or prior tooling-run result is claimed by publishing this package.

See [studio and popout research](../notes/studio-and-popout.md) and the [repository overview](../README.md).
