#!/usr/bin/env python3
"""Verify the current native atlas, animation contract and GIF timing."""

import copy
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STATES = ['idle', 'running-right', 'running-left', 'waving', 'jumping',
          'failed', 'waiting', 'running', 'review']
ONCE = {'waving', 'jumping', 'failed', 'review'}
ATLAS_SHA256 = '9e4078770ba46cd997e9fffebb6e8c4945b58a40edf224a5db855a75ca4b145c'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_manifest(manifest):
    assert manifest['id'] == 'capri' and manifest['displayName'] == 'Capri'
    assert manifest['spritesheetPath'] == 'spritesheet.webp'
    assert manifest['frame'] == {'width': 192, 'height': 208, 'columns': 16, 'rows': 35}
    assert set(manifest['animations']) == set(STATES)
    for position, state in enumerate(STATES):
        track = manifest['animations'][state]
        assert track['frames'] == list(range(position * 60, (position + 1) * 60)), state
        assert track['fps'] == 60 and track['fallback'] == 'idle', state
        assert track['loop'] is (state not in ONCE), state


def verify_native():
    release = json.loads((ROOT / 'release.json').read_text())
    assert release['version'] == '2.0.0'
    assert (release['format'], release['installFolder'], release['manifest'], release['atlas']) == (
        'codex-desktop-custom-tracks', 'capri', 'capri/pet.json', 'capri/spritesheet.webp')
    assert release['actionStates'] == STATES
    assert (release['framesPerAction'], release['configuredFps'], release['cycleMs']) == (60, 60, 1000)
    assert release['gazeCells'] == list(range(540, 556))
    assert release['gazePointerMappingVerified'] is False
    manifest = json.loads((ROOT / 'capri/pet.json').read_text())
    validate_manifest(manifest)
    negative = {}
    mutations = {
        'fps': lambda m: m['animations']['idle'].update(fps=61),
        'index': lambda m: m['animations']['idle']['frames'].__setitem__(0, 556),
        'geometry': lambda m: m['frame'].update(rows=34),
        'missing_state': lambda m: m['animations'].pop('review'),
        'duplicate': lambda m: m['animations']['idle']['frames'].__setitem__(1, 0),
        'fallback': lambda m: m['animations']['idle'].update(fallback='missing'),
    }
    for name, mutate in mutations.items():
        invalid = copy.deepcopy(manifest)
        mutate(invalid)
        try:
            validate_manifest(invalid)
        except AssertionError:
            negative[name] = 'rejected'
        else:
            raise AssertionError(f'Invalid manifest accepted: {name}')

    path = ROOT / 'capri/spritesheet.webp'
    assert digest(path) == release['atlasSha256'] == ATLAS_SHA256
    with Image.open(path) as encoded:
        assert encoded.n_frames == 1 and encoded.size == (3072, 7280)
        atlas = encoded.convert('RGBA')
    original = Image.open(ROOT / 'assets/capri.png').convert('RGBA')
    hashes = []
    for index in range(560):
        x, y = index % 16 * 192, index // 16 * 208
        cell = atlas.crop((x, y, x + 192, y + 208))
        alpha = cell.getchannel('A')
        if index >= 556:
            assert alpha.getextrema() == (0, 0), index
        elif index < 540:
            box = alpha.getbbox()
            assert box and box[0] > 0 and box[1] > 0 and box[2] < 192 and box[3] < 208, index
            hashes.append(hashlib.sha256(cell.tobytes()).hexdigest())
        else:
            gaze = index - 540
            gx, gy = gaze % 8 * 192, (9 + gaze // 8) * 208
            assert cell.tobytes() == original.crop((gx, gy, gx + 192, gy + 208)).tobytes(), index
    assert len(set(hashes)) == 540
    for position, state in enumerate(STATES):
        assert len(set(hashes[position * 60:(position + 1) * 60])) == 60, state

    gifs = []
    for name in STATES + ['all-actions']:
        gif_path = ROOT / f'media/60fps/{name}.gif'
        with Image.open(gif_path) as gif:
            assert gif.n_frames == 50, name
            delays = []
            for index in range(50):
                gif.seek(index)
                delays.append(gif.info['duration'])
            assert delays == [20] * 50, name
            size = list(gif.size)
        gifs.append({'file': str(gif_path.relative_to(ROOT)), 'bytes': gif_path.stat().st_size,
                     'sha256': digest(gif_path), 'dimensions': size, 'frames': 50,
                     'duration_ms': sum(delays), 'fps': 50})

    checksums = ROOT / 'capri/CHECKSUMS.sha256'
    entries = {}
    for line in checksums.read_text().splitlines():
        expected, name = line.split('  ', 1)
        assert name in {'pet.json', 'spritesheet.webp', 'README.txt'}
        assert digest(ROOT / 'capri' / name) == expected, name
        entries[name] = expected
    assert set(entries) == {'pet.json', 'spritesheet.webp', 'README.txt'}
    return {'ok': True, 'version': release['version'], 'atlas_sha256': digest(path),
            'atlas_bytes': path.stat().st_size, 'atlas_size': list(atlas.size),
            'action_states': 9, 'unique_action_cells': len(set(hashes)), 'frames_per_action': 60,
            'configured_fps': 60, 'action_cycle_ms': 1000, 'gaze_cells_retained_exact': 16,
            'unused_cells_transparent': 4, 'negative_controls': negative, 'gifs': gifs,
            'native_fps_measured': False, 'pointer_mapping_verified': False,
            'cli_256_cell_contract_compatible': False}


if __name__ == '__main__':
    print(json.dumps(verify_native(), indent=2))
