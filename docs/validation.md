# Validation and review

## Current release: v2.2.0

The native package contains [pet.json](../capri/pet.json) and a transparent lossless [WebP atlas](../capri/spritesheet.webp).

- Dimensions: 3072 × 7280; sixteen columns and thirty-five rows of 192 × 208 cells.
- Encoded size: 17,389,670 bytes.
- SHA-256: `4d505451682db28fdcad641a4a8489676ca1d63853ddb731cd2d95dde46e41ff`.
- Cells 60–179: the two self-lightning travel tracks, 60 unique frames each.
- The other 436 occupied cells match v2.1.0 exactly; four unused cells remain transparent.

All nine actions retain 60 frames at a configured 60 fps for one second. Greeting, lift, failure and review play once with an idle fallback; the other states loop. The native manifest, pet ID, metadata, indices and state semantics are unchanged.

## Transformation and preservation checks

Codex's `running-right` and `running-left` states select the new travel tracks. Each shows a voluntary smiling transformation into her own red form, a directional streak and calm reformation. It repeats while the travel state is active. No random, speed-based or failure trigger was added. State transitions remain under Codex's control.

The right track copies the corrected 60-frame preview pixels exactly. The left track uses separately generated complete poses, preserving normal green/pink body regions rather than mirroring them. Two early normal drawings were placed after the red span; all sixty drawings are used once. Assembly only extracts, chroma-cleans, uniformly fits and places whole generated drawings. No body warps, optical-flow frames or code-painted lightning are used.

Source-to-frame checks reproduce the left pixels and verify the exact right source frames. Every encoded atlas cell matches its assembly hash. Tests measure a continuous full-red phase and colored normal endpoints in both tracks. The coordinator inspected every final travel pose and both directions' expressions; this is self-review, not independent review or new owner aesthetic acceptance. The other seven actions and sixteen gaze drawings are checked against their previous hashes.

## Preview and package checks

Transparent masters have 60 lossless frames with 16/17 ms delays totaling 1000 ms. Action GIFs use 50 samples at 20 ms each, preserving the same one-second cycle. GIFs are not 60 fps. Travel GIF pixels match the native cells after display scaling and palette quantization. The unchanged gaze GIF has sixteen poses over two seconds.

Isolated Chrome loaded the actual encoded atlas and showed advancing left/right, all-action and paired-direction GIFs without page or request errors. The unchanged gaze receipt is reused by matching its file hash. These checks are not a desktop-overlay recording or native FPS benchmark.

Maintainer checks require Python, Pillow, FFmpeg and ffprobe. Run `python3 scripts/build_release.py` to refresh the ZIP, checksums, GIF inventory and validation; run `python3 scripts/verify_assets.py` for the full repository check. The large static lossless atlas is decoded through FFmpeg and read one cell at a time. These tools are not needed to install or run the pet.

Checks cover 540 unique action cells, sixteen gaze cells, all 556 assembly hashes, four empty cells, source provenance, safe alpha bounds, exact preservation of 436 unrelated cells, manifest paths/indices/fps/loops/fallbacks and GIF timing. Six invalid-manifest controls must fail; another control changes an unrelated cell and must fail preservation validation. ZIP CRC and exact entry hashes must pass. The ZIP contains only manifest, atlas, instructions and checksums. Documentation links, repository checksums and private-content patterns are also checked.

See [native validation](../qa/native-validation.json), [integration contract](../qa/lightning-integration.json), [source provenance](../qa/native-color-provenance.json), [browser check](../qa/native-browser-playback.json) and [checksums](../SHA256SUMS.txt).

## Compatibility and rollback

This update has not been installed in the owner's Windows app. No instrumented desktop FPS, resource-use or latency measurement was made. Display cadence depends on the app and device. Native gaze pointer mapping remains unverified.

The package targets Codex desktop builds that accept this custom-track atlas. The smaller CLI format and managed ChatGPT Pets use different contracts; no app binary or guard was patched. The [v2.1.0 release](https://github.com/Zack24680/capri-pet/releases/tag/v2.1.0) preserves the corrected colors and previous glides for rollback. Earlier releases and legacy PNG/player/media files remain historical material.
