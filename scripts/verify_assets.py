#!/usr/bin/env python3
"""Verify the distributed artwork, metadata, media and public file inventory."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".capture", "dist", "__pycache__", ".venv"}


def public_files():
    return sorted(p for p in ROOT.rglob("*") if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(ROOT).parts))


def verify():
    metadata = json.loads((ROOT / "metadata.json").read_text())
    sprite = ROOT / metadata["sprite"]["file"]
    digest = hashlib.sha256(sprite.read_bytes()).hexdigest()
    assert digest == metadata["sprite"]["sha256"]
    image = Image.open(sprite).convert("RGBA")
    assert image.size == (1536, 2288)
    counts = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
    used, unused = 0, 0
    for row, count in enumerate(counts):
        for column in range(8):
            cell = image.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
            if column < count:
                assert cell.getchannel("A").getbbox(), (row, column, "blank")
                used += 1
            else:
                assert cell.getchannel("A").getextrema() == (0, 0), (row, column, "unused artwork")
                unused += 1
    assert (used, unused) == (73, 15)
    legacy = Image.open(ROOT / "assets/capri-v1.png").convert("RGBA")
    assert legacy.size == (1536, 1872)
    assert legacy.tobytes() == image.crop((0, 0, 1536, 1872)).tobytes()
    for name in ["atlas-validation.json", "atlas-validation-v1.json", "quality-validation.json"]:
        assert json.loads((ROOT / "qa" / name).read_text())["ok"] is True
    assert json.loads((ROOT / "qa/pets-preflight.json").read_text())["valid"] is True
    for state in metadata["states"]:
        gif = Image.open(ROOT / "media/states" / f"{state['id']}.gif")
        assert gif.n_frames == state["frames"]
        duration = 0
        for index in range(gif.n_frames):
            gif.seek(index)
            duration += gif.info["duration"]
        assert duration == state["cycleMs"] == sum(state["durationsMs"])
    assert Image.open(ROOT / "media/look-loop.gif").n_frames == 16
    assert Image.open(ROOT / "media/all-states.gif").n_frames == 114
    js = (ROOT / "preview/metadata.js").read_text()
    assert json.loads(js.removeprefix("window.CAPRI_METADATA = ").strip().removesuffix(";")) == metadata
    expected_angles = ["000", "022.5", "045", "067.5", "090", "112.5", "135", "157.5", "180", "202.5", "225", "247.5", "270", "292.5", "315", "337.5"]
    assert [look["angle"] for look in metadata["looks"]] == expected_angles
    for name in ["capri-demo.mp4", "capri-demo.webm", "screenshot-player.png", "screenshot-nine-states.png", "screenshot-gaze.png"]:
        assert (ROOT / "media" / name).stat().st_size > 0
    browser = json.loads((ROOT / "qa/browser-playback.json").read_text())
    assert not browser["page_errors"] and not browser["failed_requests"]
    assert len(browser["tested_states"]) == 9 and browser["look_cells"] == 16
    broken, private = [], []
    forbidden = re.compile(r"/home/[^/\s]+/|/Users/[^/\s]+/|pet_[0-9a-f]{20,}|upload_session_id|gh[pousr]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,}")
    # Inspect public content, excluding the literal scan patterns in this verifier.
    for path in public_files():
        if path.suffix in {".md", ".json", ".html", ".js", ".css", ".txt", ".py"}:
            value = path.read_text()
            if path != Path(__file__).resolve() and forbidden.search(value):
                private.append(str(path.relative_to(ROOT)))
            if path.suffix == ".md":
                for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", value):
                    if target.startswith(("https://", "http://", "#", "mailto:")):
                        continue
                    target = unquote(target.split("#", 1)[0])
                    if not (path.parent / target).resolve().exists():
                        broken.append((str(path.relative_to(ROOT)), target))
        if path.suffix == ".png":
            for value in Image.open(path).info.values():
                if isinstance(value, str) and forbidden.search(value):
                    private.append(str(path.relative_to(ROOT)))
    assert not broken, broken
    assert not private, private
    checksums = ROOT / "SHA256SUMS.txt"
    if checksums.exists():
        entries = {}
        for line in checksums.read_text().splitlines():
            expected, name = line.split("  ", 1)
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
            entries[name] = expected
        assert set(entries) == {str(p.relative_to(ROOT)) for p in public_files() if p != checksums}
    return {"ok": True, "sprite_sha256": digest, "required_cells": used, "transparent_unused_cells": unused,
            "lossless_v1_crop": True, "state_gifs": 9, "look_frames": 16,
            "local_markdown_links": "passed", "private_content_scan": "passed", "checksums": checksums.exists()}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
