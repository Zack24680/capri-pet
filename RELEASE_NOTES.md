# Capri v2.2.0 — self-lightning travel

Capri now becomes her own smiling red-lightning form during both directional travel animations, then reforms calmly. The right track uses the corrected transformation preview; the left track has separately generated left-facing drawings that preserve her normal color asymmetry.

**When it happens:** Codex selects the `running-right` or `running-left` travel state. Each track contains 60 distinct frames over one second at a configured 60 fps, repeating while that state remains active. No random, speed-threshold or failure trigger was added. The other seven actions and all sixteen gaze cells are unchanged from v2.1.0.

[Download capri-60fps.zip](https://github.com/Zack24680/capri-pet/releases/download/v2.2.0/capri-60fps.zip), back up your existing Capri folder, then follow the [installation instructions](https://github.com/Zack24680/capri-pet#install-in-codex). The ZIP contains only the four native installation files. The README showcases the actual released atlas with GIFs at the same cycle speed.

Checks cover all 556 occupied cells, exact preservation of 436 unrelated cells, full red phases and normal endpoints in both tracks, source pixels, GIF timing, lossless masters, browser playback, six invalid manifest controls, a changed-cell preservation control and ZIP integrity. This update has not been installed in the owner's Windows app; configured 60 fps is not a measured desktop frame rate.

[v2.1.0](https://github.com/Zack24680/capri-pet/releases/tag/v2.1.0) remains available for rollback. See [validation](https://github.com/Zack24680/capri-pet/blob/main/docs/validation.md) for evidence and limits.
