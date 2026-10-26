#!/usr/bin/env python3
"""Build the current install-only release and refresh portable verification."""

import hashlib
import json
from pathlib import Path
import zipfile

from verify_assets import ROOT, public_files, verify
from verify_native import verify_native


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    folder = ROOT / 'capri'
    native_files = [folder / name for name in ['pet.json', 'spritesheet.webp', 'README.txt']]
    checksum = folder / 'CHECKSUMS.sha256'
    checksum.write_text(''.join(f'{sha(p)}  {p.name}\n' for p in native_files))
    result = verify_native()
    (ROOT / 'qa/native-validation.json').write_text(json.dumps(result, indent=2) + '\n')
    (ROOT / 'qa/native-media-inventory.json').write_text(json.dumps({'media': result['gifs']}, indent=2) + '\n')
    lines = ['# Current GIF inventory', '',
             'These v2.2.0 GIFs show the released artwork, including self-lightning in both travel directions. Action previews use 50 frames at 20 ms, preserving the native one-second cycle; native tracks use all 60 frames at a configured 60 fps. The gaze preview cycles through sixteen discrete poses over two seconds using 120/130 ms delays.', '',
             '| File | Bytes | Dimensions | Timing |', '| --- | ---: | --- | --- |']
    for item in result['gifs']:
        width, height = item['dimensions']
        lines.append(f"| [{Path(item['file']).name}](../{item['file']}) | {item['bytes']:,} | {width} × {height} | {item['frames']} frames / {item['duration_ms']/1000:.2f} s |")
    lines += ['', 'The install ZIP contains only the native pet folder: manifest, lossless atlas, instructions and checksums. Historical v1.0.0 media elsewhere in the repository describes the earlier artwork.', '']
    (ROOT / 'docs/media-inventory.md').write_text('\n'.join(lines))
    checksums = ROOT / 'SHA256SUMS.txt'
    entries = [p for p in public_files() if p != checksums]
    checksums.write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT)}\n' for p in entries))
    verification = verify()

    output = ROOT / 'dist/capri-60fps.zip'
    output.parent.mkdir(exist_ok=True)
    native_files.append(checksum)
    expected = {f'capri/{p.name}': sha(p) for p in native_files}
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in native_files:
            entry = zipfile.ZipInfo(f'capri/{path.name}', date_time=(2026, 10, 27, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == 4 and set(archive.namelist()) == set(expected)
        for name, expected_hash in expected.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected_hash, name
    (output.parent / 'SHA256SUMS.txt').write_text(f'{sha(output)}  {output.name}\n')
    print(json.dumps({'ok': verification['ok'], 'native_states': result['action_states'],
                      'unique_action_frames': result['unique_action_cells'],
                      'negative_controls': result['negative_controls'],
                      'archive': output.name, 'bytes': output.stat().st_size,
                      'sha256': sha(output), 'entries': 4}, indent=2))


if __name__ == '__main__':
    build()
