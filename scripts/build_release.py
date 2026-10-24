#!/usr/bin/env python3
"""Create a portable media inventory, checksums and complete release ZIP."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

from PIL import Image
from verify_assets import ROOT, public_files, verify


def build():
    rows = []
    for path in sorted((ROOT / "media").rglob("*")):
        if not path.is_file():
            continue
        item = {"file": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        if path.suffix in {".png", ".gif"}:
            image = Image.open(path)
            item.update(width=image.width, height=image.height)
            if path.suffix == ".gif":
                duration = 0
                for index in range(image.n_frames):
                    image.seek(index)
                    duration += image.info.get("duration", 0)
                item.update(frames=image.n_frames, duration_ms=duration)
        elif path.suffix in {".mp4", ".webm"}:
            result = json.loads(subprocess.check_output([
                "ffprobe", "-v", "error", "-show_entries",
                "stream=codec_name,width,height,r_frame_rate:format=duration", "-of", "json", str(path)]))
            stream = result["streams"][0]
            item.update(codec=stream["codec_name"], width=stream["width"], height=stream["height"],
                        encoded_frame_rate=stream["r_frame_rate"], duration_seconds=float(result["format"]["duration"]))
        rows.append(item)
    (ROOT / "qa/media-inventory.json").write_text(json.dumps({"media": rows}, indent=2) + "\n")
    lines = ["# Media inventory", "", "Measured from the distributed files with Pillow and FFprobe. Encoded video frame rate describes the recording/container, not the authored sprite cadence or ChatGPT app performance.", "", "| File | Size (bytes) | Dimensions | Playback |", "| --- | ---: | --- | --- |"]
    for item in rows:
        duration = (f"{item['duration_ms'] / 1000:.2f} s / {item['frames']} frames" if "duration_ms" in item else
                    f"{item['duration_seconds']:.2f} s / {item['codec']}" if "duration_seconds" in item else "still")
        lines.append(f"| [{Path(item['file']).name}](../{item['file']}) | {item['bytes']:,} | {item['width']} × {item['height']} | {duration} |")
    lines += ["", "The recorded demo is an isolated browser capture of the included player. The MP4 is a trimmed H.264 encoding of that capture; the original WebM retains the setup/check prelude. Compact `all-states.mp4` was encoded from the all-state GIF and has slightly different container timing.", ""]
    (ROOT / "docs/media-inventory.md").write_text("\n".join(lines))
    checksums = ROOT / "SHA256SUMS.txt"
    # Refresh, rather than validating a previous manifest after new files were recorded.
    entries = [p for p in public_files() if p != checksums]
    checksums.write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + str(p.relative_to(ROOT)) + "\n" for p in entries))
    result = verify()
    version = json.loads((ROOT / "metadata.json").read_text())["version"]
    output = ROOT / "dist" / f"capri-pet-v{version}.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in public_files():
            archive.write(path, str(Path("capri-pet") / path.relative_to(ROOT)))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert archive.read("capri-pet/assets/capri.png") == (ROOT / "assets/capri.png").read_bytes()
    print(json.dumps({"verification": result, "archive": output.name, "archive_bytes": output.stat().st_size,
                      "archive_sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "files": len(public_files())}, indent=2))


if __name__ == "__main__":
    build()
