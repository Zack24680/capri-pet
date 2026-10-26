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
    assert release['version'] == '2.1.0'
    assert (release['format'], release['installFolder'], release['manifest'], release['atlas']) == (
        'codex-desktop-custom-tracks', 'capri', 'capri/pet.json', 'capri/spritesheet.webp')
    assert release['actionStates'] == STATES
    assert (release['framesPerAction'], release['configuredFps'], release['cycleMs']) == (60, 60, 1000)
    assert release['gazeCells'] == list(range(540, 556))
    assert release['gazePointerMappingVerified'] is False
    assert release['bodyColorsCorrected'] is True and release['gazeColorsCorrected'] is True
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
    provenance = json.loads((ROOT / 'qa/native-frame-hashes.json').read_text())
    assert provenance['version'] == release['version']
    assert digest(path) == release['atlasSha256'] == provenance['atlas_sha256']
    expected_cells = provenance['cell_rgba_sha256']
    assert len(expected_cells) == len(set(expected_cells)) == 556
    color_sources = json.loads((ROOT / 'qa/native-color-provenance.json').read_text())
    source_summary = json.loads((ROOT / 'qa/native-provenance.json').read_text())
    assert color_sources['version'] == source_summary['version'] == release['version']
    assert set(color_sources['cell_sources']) == set(STATES + ['gaze'])
    for position, state in enumerate(STATES + ['gaze']):
        source_cells = color_sources['cell_sources'][state]
        start, count = (540, 16) if state == 'gaze' else (position * 60, 60)
        assert len(source_cells) == count
        assert [cell['rgba_sha256'] for cell in source_cells] == expected_cells[start:start + count]
        for cell in source_cells:
            assert cell['source_sha256'] == source_summary['selected_source_sha256'][cell['asset']]
            assert cell['asset'] == state or (state in {'idle', 'running-right'} and cell['asset'] == 'border-repair')
            assert cell['scale'] > 0 and isinstance(cell['source_index'], int)
    with Image.open(path) as encoded:
        assert encoded.n_frames == 1 and encoded.size == (3072, 7280)
        atlas = encoded.convert('RGBA')
    hashes = []
    for index in range(560):
        x, y = index % 16 * 192, index // 16 * 208
        cell = atlas.crop((x, y, x + 192, y + 208))
        alpha = cell.getchannel('A')
        if index >= 556:
            assert alpha.getextrema() == (0, 0), index
        else:
            box = alpha.getbbox()
            assert box and box[0] > 0 and box[1] > 0 and box[2] < 192 and box[3] < 208, index
            cell_hash = hashlib.sha256(cell.tobytes()).hexdigest()
            assert cell_hash == expected_cells[index], index
            hashes.append(cell_hash)
    assert len(set(hashes[:540])) == 540 and len(set(hashes[540:])) == 16
    for position, state in enumerate(STATES):
        assert len(set(hashes[position * 60:(position + 1) * 60])) == 60, state

    gifs = []
    for name in STATES + ['all-actions', 'gaze']:
        gif_path = ROOT / f'media/60fps/{name}.gif'
        with Image.open(gif_path) as gif:
            count, delay = (16, 125) if name == 'gaze' else (50, 20)
            assert gif.n_frames == count, name
            delays = []
            for index in range(count):
                gif.seek(index)
                delays.append(gif.info['duration'])
            expected_delays = [(round((i+1)*200/16)-round(i*200/16))*10 for i in range(16)] if name == 'gaze' else [delay]*count
            assert delays == expected_delays, name
            size = list(gif.size)
        gifs.append({'file': str(gif_path.relative_to(ROOT)), 'bytes': gif_path.stat().st_size,
                     'sha256': digest(gif_path), 'dimensions': size, 'frames': count,
                     'duration_ms': sum(delays), 'fps': 1000 / delay})

    browser = json.loads((ROOT / 'qa/native-browser-playback.json').read_text())
    assert browser['atlas_sha256'] == digest(path)
    assert browser['owned_browser_closed'] and not browser['page_errors'] and not browser['failed_requests']
    assert {item['file'] for item in browser['gifs']} == {'media/60fps/all-actions.gif', 'media/60fps/gaze.gif'}
    for item in browser['gifs']:
        assert item['distinct_screenshot_samples'] > 3
        assert item['sha256'] == digest(ROOT / item['file'])

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
            'action_states': 9, 'unique_action_cells': len(set(hashes[:540])), 'frames_per_action': 60,
            'configured_fps': 60, 'action_cycle_ms': 1000, 'gaze_cells_corrected': 16,
            'all_556_cells_match_assembly_hashes': True,
            'unused_cells_transparent': 4, 'negative_controls': negative, 'gifs': gifs,
            'native_fps_measured': False, 'pointer_mapping_verified': False,
            'cli_256_cell_contract_compatible': False}


if __name__ == '__main__':
    print(json.dumps(verify_native(), indent=2))
