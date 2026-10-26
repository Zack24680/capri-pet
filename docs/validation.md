# Validation and review

## Current release: v2.1.0

The native package contains [pet.json](../capri/pet.json) and a transparent lossless [WebP atlas](../capri/spritesheet.webp).

- Dimensions: 3072 × 7280; sixteen columns and thirty-five rows of 192 × 208 cells.
- Encoded size: 17,221,638 bytes.
- SHA-256: `5033ea3eb81c73463275c44b26fba64cc247e793fd7c708f55983dfb3cf54e40`.
- Cells 0–539: nine actions, 60 distinct frames each; 540 unique action frames.
- Cells 540–555: sixteen corrected gaze poses in the original angular order.
- Cells 556–559: transparent unused cells.

Every action uses 60 frames at a configured 60 fps for one second. Greeting, lift, failure and review play once with an idle fallback; the other states loop. Existing state semantics and separate directional drawings are retained.

## Artwork checks

The pink torso/hip motif and asymmetric green/pink limb fields were corrected throughout the release, retaining the dark breaks, purple edges, pink texture and rounded silhouette. The coordinator inspected every final action/gaze contact sheet, including before/during/after glitch expressions. This is self-review, not independent review or new owner acceptance. Some frame-to-frame drawing variation remains.

The drawings came from OpenAI's built-in image generator. Source/component receipts verify retained complete poses. The final ten idle and right-glide poses received generated foot-tip boundary completion. Two greeting drawings connected only by faint edge fringe were separated using their disconnected opaque cores; all retained original RGBA values stayed unchanged. An extra source greeting pose was excluded in chronological selection. Failed repair attempts were not integrated.

Assembly uses uniform source calibration, a common fit and whole-pose head registration to the accepted prior motion path. No body/face warps, optical flow, synthetic in-betweens or code-painted color patterns/glitch art are used. Full transparent masters have 60 lossless frames with 16/17 ms delays totaling 1000 ms. Every master frame was reproduced from its source crop/transform and compared with the decoded atlas cell. [Per-cell hashes](../qa/native-frame-hashes.json) and [source provenance](../qa/native-color-provenance.json) record the corrected 556 cells, including the new gaze artwork.

## Preview and package checks

Action GIFs sample 50 frames at 20 ms each, retaining the one-second cycle speed. GIFs are not 60 fps. The gaze GIF cycles 16 discrete poses over two seconds with 120/130 ms delays. Isolated Chrome loaded the actual encoded atlas and showed advancing action/gaze GIFs without page or request errors. This browser check is not a desktop-overlay capture or runtime benchmark.

Run `python3 scripts/build_release.py` with Pillow to refresh the install ZIP, checksums, GIF inventory and native validation. Run `python3 scripts/verify_assets.py` to check the current package and preserved legacy files. Checks cover geometry, safe alpha bounds, 540 unique action cells, 16 unique corrected gaze cells, all 556 assembly hashes, transparent unused cells, track indices/fps/loops/fallbacks and GIF timing. Six invalid-manifest controls test fps, indices, geometry, missing states, duplicate indices and invalid fallbacks; each must fail.

The ZIP passes CRC and exact entry-hash checks. It contains only four installation files: manifest, atlas, instructions and checksums. Repository checks cover local Markdown links, published checksums and machine-local path/secret patterns. See [native validation](../qa/native-validation.json), [browser check](../qa/native-browser-playback.json) and [checksums](../SHA256SUMS.txt).

## Compatibility and rollback

The owner previously tried the v2.0.0 motion package. This v2.1.0 color revision has not been installed in the owner's desktop app. No instrumented desktop FPS, resource-use or latency measurement was made. Actual displayed cadence depends on the app and device. Gaze pointer mapping remains unverified.

This larger custom-track atlas targets compatible Codex desktop builds. The known CLI format has a 256-cell limit; managed ChatGPT Pets use another fixed format. No app binary or guard was patched.

Historical [v2.0.0](https://github.com/Zack24680/capri-pet/releases/tag/v2.0.0) and [v1.0.0](https://github.com/Zack24680/capri-pet/releases/tag/v1.0.0) releases remain unchanged. Legacy PNGs, root metadata, older browser preview and older QA/media describe previous artwork; they are not the current install atlas or validation evidence for its corrected colors.
