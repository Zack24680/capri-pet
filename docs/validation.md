# Validation and review

## Current release: v2.0.0

The native package uses [pet.json](../capri/pet.json) and a lossless [WebP atlas](../capri/spritesheet.webp). The atlas is the same encoded artwork supplied in the accepted motion candidate:

- Dimensions: 3072 × 7280; sixteen columns and thirty-five rows of 192 × 208 cells.
- Encoded size: 17,671,022 bytes.
- SHA-256: `9e4078770ba46cd997e9fffebb6e8c4945b58a40edf224a5db855a75ca4b145c`.
- Cells 0–539: nine actions with 60 distinct frames each; 540 unique action frames in total.
- Cells 540–555: sixteen original gaze drawings, retained pixel-exact.
- Cells 556–559: fully transparent unused cells.

Every action track has 60 frames at 60 fps, for a one-second cycle. Greeting, lift, failure and review play once with an idle fallback. Idle, directional glides, input and work loop. The release manifest has separate tracks for these behaviors; it is not the temporary diagnostic tour.

## Artwork and timing checks

Source extraction and final encoding were checked for complete poses, alpha bounds, unique frames and exact decoded equality. Transparent animated WebP masters have 60 frames with 16/17 ms delays totaling 1000 ms. Public GIF previews sample 50 of those frames at 20 ms each, preserving the one-second action cycle. GIFs are not labeled 60 fps.

The new poses and glitches were generated with OpenAI's built-in image generator. Assembly applies uniform source calibration, a common fit, head/body registration and authored whole-pose hover or levitation placement. No face/body warps, optical-flow in-betweens, crossfades or code-drawn glitch art were used.

The measured body lift is approximately 12.56 px. The lift's body anchor differs from idle by approximately 0.62 px on entry and 0.97 px on return. Curled legs change the lowest foot pixel by 7 px; this floating character has no fixed floor baseline. These are visible-pixel measurements, not motion-capture data.

The coordinator inspected source and final encoded samples, directional gestures, glitch-before/during/after samples, the lift transition and all sixteen retained gaze poses. The owner subsequently tried the revision and accepted its appearance. This is coordinator self-review plus owner feedback, not independent review. Some frame-to-frame drawing variation remains.

## Reproducible package checks

`python3 scripts/build_release.py` uses Pillow to build the install-only ZIP and refresh the checksums, current GIF inventory and verification report. `python3 scripts/verify_assets.py` verifies both the native release and preserved legacy files.

The native checks read the actual atlas and verify geometry, alpha bounds, all 540 unique action cells, exact original gaze retention, empty unused cells, manifest paths/indices/fps/loops/fallbacks and GIF frame durations. Six negative controls deliberately supply invalid fps, indices, geometry, missing states, duplicate indices and invalid fallbacks; each must fail. The ZIP passes CRC and exact entry-hash comparisons and contains only the four installation files.

The whole-repository check also verifies local documentation links, all published checksums and absence of machine-local paths or known secret patterns. See [native validation](../qa/native-validation.json), [provenance](../qa/native-provenance.json) and [checksums](../SHA256SUMS.txt).

## Compatibility and evidence limits

The owner reported a working-looking desktop trial; the exact client version was not supplied. No instrumented desktop FPS, resource use or input-latency measurement was made. Configuring 60 fps and verifying encoded timelines does not establish a device's displayed frame cadence.

The known CLI format has a 256-cell limit and cannot accept this larger atlas. The managed ChatGPT Pets upload uses a different fixed format. This package targets Codex desktop builds that accept its custom animation tracks; it is not a universal CLI or managed-upload package. No application binary, validator or guard was patched.

The sixteen gaze drawings remain in the atlas, but native pointer mapping and 60 fps gaze interpolation are not verified. Discrete gaze artwork does not imply continuous 3D tracking.

## Preserved v1.0.0 material

The original [PNG](../assets/capri.png) and its v1 compatibility crop remain unchanged, as does the historical v1.0.0 release. Root `metadata.json`, the older browser preview and the original QA reports describe that earlier artwork. Their fixed-format Pets preflight and older motion measurements do not validate this new native atlas.
