# Evidence, measurement and completion

## Full acceptance gate

**Open review findings:** the checker is not yet a sufficient standalone gate. Read [review-findings.md](review-findings.md) before relying on an exit code.

All 60 requirements and all 80 required test variants must be satisfied against the same implementation/engine revisions and contract SHA-256. A missing/blocked/not_run/partial/failed/skipped result is **not accepted**. The eight supplied browser cases are necessary but insufficient for full acceptance.

The completion checker validates identity, coverage, evidence presence/hashes, required evidence kinds and numeric rules. It does not cryptographically prove that an operator's recorded observation is true. Review artifacts and independently measured outputs as part of T039/T040. Do not treat an AI-written ledger or an application diagnostic counter as independent proof.

## Evidence hierarchy

| Evidence | Establishes | Does not establish |
|---|---|---|
| Browser suite / screenshot | User controls, navigation, labels and UI workflows | Guest exclusion from actual output, call latency, physical phone behavior |
| Application diagnostic snapshot | Internal identity/state/counters, correlated with other evidence | Actual receiver frames, true absence of leaked audio, successful buyer playback |
| Output protocol/network summary | Attempted negotiation, session status, request timing and endpoint handling | Usable media by itself |
| Independent receiver recording + analysis | Actual decoded program image/audio and transitions | Native mobile device behavior or platform buyer integration by itself |
| Physical-device capture and device record | Actual browser/OS/device permission/audio/lifecycle behavior | Every other browser/device or production reliability |
| Real QA buyer recording | Correct event/seller context and observed delivered program | A low-latency ingest/call guarantee or production readiness |

## Ledger format

From this package directory, use `python validation/completion.py init --out validation/runs/my-run/ledger.json`. It creates **not_run** records, never successful placeholders. The ledger contains:

```json
{
  "schemaVersion": 1,
  "contractVersion": "1.0.0",
  "contractSha256": "<actual contract.json sha256>",
  "run": {
    "implementationRevision": "<commit/build digest>",
    "engineRevision": "<pinned engine commit/build digest>",
    "environmentKind": "local-and-qa",
    "executedBy": "<operator or agent identity>",
    "startedAt": "<UTC ISO timestamp>",
    "finishedAt": "<UTC ISO timestamp>",
    "browserVersions": {"hostChrome": "...", "hostEdge": "..."},
    "deviceRecords": ["<physical Android record>", "<physical iPhone record>"],
    "fixtureDescription": "<source identities, timing method, hardware/network>"
  },
  "results": [
    {
      "testId": "T006",
      "variant": "default",
      "status": "not_run",
      "observations": "",
      "metrics": {},
      "evidence": []
    }
  ]
}
```

Each evidence entry has `kind`, a file `path` relative to the ledger directory, and `sha256`. The checker refuses path traversal/outside-root symlinks, missing/empty files, duplicate result keys, mismatched hashes or unrecognized cases. Artifacts may be reused where they truly contain the required observation, with interval/stream/revision references in observations. Required kinds are listed per scenario.

For a measurement record, preserve the raw recording/report and the analysis command, interval and assumptions. A manually copied number without its source artifact is insufficient. The `media-analysis` evidence must be an actual JSON report with `sourceSha256`, `analysisWindow`, `metrics` and tool identity; the checker validates its recording hash and metadata. A raw receiver recording is not a screenshot of the application's preview.

Native Playwright output can be associated with browser cases using `completion.py import-browser`; only the eight supplied browser case IDs may be imported. Assisted/manual cases remain not_run until actually executed and documented. A browser run that returns green by skipping tests does not import as a pass.

## Controlled source fixtures and analysis

The generated laboratory cameras are moving red-tinted host and blue-tinted guest inputs with 440 Hz and 880 Hz tones. The colors/tones originate in the input media, not as overlays added by the program; this prevents a fabricated layout label from masquerading as a received guest. Fake inputs prove controlled workflows/media only, not physical capture or echo cancellation.

`validation/analyze_media.py` decodes a recording with FFmpeg, measures red/blue occupancy and tone levels for a declared interval, and writes a SHA-bound JSON report. It is a partial measurement tool: it does **not** alone establish layout geometry, frame-rate/freeze timing, A/V alignment, echo cancellation, physical devices or buyer identity. Those need their scenario's additional reports and artifact review.

For isolation cases, use stable intervals after the declared startup/transition grace. Guest blue occupancy <=0.001 and 880 Hz component <=-55 dBFS are the baseline absence thresholds; host and admitted guest presence thresholds are in the contract. Do not silently alter thresholds to accommodate a failed mix. Program-ingress cutoff and viewer-arrival delay are separate measurements.

## Frame rate, freezes and soak

- Record the actual decoded receiver program continuously for the soak, with sender/receiver diagnostics and a monotonic source-motion/frame marker.
- Report decoded fps **and moving-source continuity**. Repeated encoded frames or app-generated frame counters do not prove fresh source frames.
- Identify any freeze >1000 ms during normal operation. Label injected faults before analysis; do not remove accidental failures from normal windows afterward.
- Run for at least 1800 seconds. Record hardware, OS, browser versions, capture/output sizes, codec, bitrate and network profile.
- After a five-minute warmup, compare renderer JS heap median in the next five-minute window with the final five-minute window. Growth must be <=100 MiB, with queue depths bounded and at most one active publisher. Do not force garbage collection to manufacture a passing trend.

## Timing and audio

Use synchronized flash/audio pulses and shared-clock filming or another method with bounded uncertainty. Collect at least 30 samples. Report p95 absolute A/V skew, one-way call delay and local program delay with the analysis method. A ping/RTT number is not a glass-to-glass media delay measurement. Browser clocks on different machines are not assumed synchronized.

Control the lab network (<=20 ms added RTT, no induced loss for the normal timing case). Record audience CDN delay independently and do not apply the call/ingest budget to buyer delivery. Use physical-phone headphone and speaker runs to identify self-return, echo and duplicate capture that synthetic headless tones do not establish.

## Real devices, PiP and network route

Record physical model, OS/browser version, capture route and test date for both Android Chrome and iPhone Safari. Playwright viewport/device emulation is explicitly insufficient. Run PiP in headed Chrome and Edge; capture the actual floating window and correlated receiver program. A DOM card labeled PiP does not pass.

Forced TURN requires actual selected `relay` candidate-pair evidence and working media. Direct evidence requires the selected direct route. Missing TURN/device/QA access stays BLOCKED and prevents full acceptance.

## Privacy and storage

Keep auth state, invite capabilities, real ingest credentials, raw traces and recordings in private run folders excluded from version control. Redact secret values from shareable summaries. Expire/revoke disposable invites after tests. Do not upload private host application source, raw design research, real tokens or test recordings to the public concept repo. No production event or real bid/purchase is part of this contract.


## Public scope and references

This is a proposed engineering contract, not an approved product specification or a claim about a deployed system. Internal source maps, source revisions, private research, service locations and run artifacts are intentionally not distributed. See [public studio research](../notes/studio-and-popout.md), [integration responsibilities](integration-map.md), and [open review findings](review-findings.md).

Return to [package overview](README.md).
