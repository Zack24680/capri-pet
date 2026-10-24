# Validation and review

## Published bytes

The V2 sheet is the exact PNG accepted by the owner after inspecting the final motion:

- Dimensions: 1536 × 2288; RGBA; 2,414,151 bytes.
- SHA-256: `cfd4a14f51dde57049bad38da9cd5e65f5434466256edfa339d0ac5f3f4d0ae6`.
- Eight columns and eleven rows with 192 × 208 cells.
- 73 required populated cells; 15 unused cells fully transparent.

The V1 compatibility file is a lossless crop of rows 0–8 from these exact bytes. It contains the same 57 standard poses and omits the sixteen look poses. Its own structural validation is saved separately.

## Checks performed

1. Every standard source strip passed bundled connected-pose extraction and immediate inspection; the combined standard frame review also passed.
2. Four cardinal anchors were inspected before the sweep. The gaze rows were generated as coherent eight-pose groups and reviewed in fixed clockwise order.
3. Registration used one common transform across the final sixteen look poses, including the lifted-head endpoint. Individual final cells were not resized or retouched to conceal failures.
4. A single chroma-edge cleanup pass was applied to the final newly assembled raw revision. Exact encoded bytes passed the structural validator and quality gate.
5. The Pets service returned `valid: true` for the same V2 file. Creation and listing were verified; private service/account identifiers are excluded from publication.
6. All-state, per-state, native jump and look previews were rendered from the final encoded atlas. The owner explicitly accepted the final visual result after gaze repairs. This was coordinator review plus owner inspection, not an independent reviewer panel.
7. The public player is checked in an isolated browser: all nine state selectors, sixteen gaze cells, pause/resume, native and enlarged scale, and absence of page errors or failed local requests.

## Measured motion properties

The validator reports an idle foot/base baseline of 202 px. Jump baselines are `[202, 193, 164, 202, 202]`, giving 38 px of lift and zero final landing difference. These are visible-pixel geometric measurements; they do not claim motion-capture accuracy.

The maximum horizontal look-center displacement from idle is 6.5 px. The widest/narrowest look silhouette ratio is approximately 1.054. These are bounds-based consistency measures, not proof of semantic direction on their own.

## Retained review warnings

The final quality report is `ok: true` with no errors. It retains reviewed warnings:

- Intermediate directions 022.5, 045, 157.5, 202.5 and 337.5 have subtle axis cues.
- Isolated transparent interior-row measurements occur in 180 and 247.5. They did not meet the hard multi-row material-hole failure rule.
- Continuity difference outliers occur at 067.5→090 and the row/wrap boundaries 157.5→180 and 337.5→000.

These warnings are disclosed rather than rewritten as a zero-warning claim. The labeled sheet, ordered loop, actual numeric reports and accepted visuals remain available for inspection.

## Portable evidence

The reports under `qa/` retain measured results while replacing machine-local file labels with repository-relative names. They are portable copies of the recorded evidence, not an assertion that their original generating tools are vendored here. The original bundled Pets validators remain part of their installed plugin distribution.

`scripts/verify_assets.py` checks the distributed bytes, cell occupancy, transparent unused cells, the lossless V1 crop, metadata, media properties/checksums and local documentation links. It does not replace the original semantic/art review or claim to measure host-app behavior.

## Performance limits

Playback durations, encoded sizes, geometry and media properties are measured. No host CPU/RAM, input latency, ChatGPT overlay FPS or platform-wide resource benchmark was recorded. The browser recording demonstrates the supplied player, not an installed pet's behavior in every client. Sixteen discrete look poses do not imply continuous 3D tracking.
