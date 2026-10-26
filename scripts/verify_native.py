#!/usr/bin/env python3
"""Verify the current native atlas, animation contract and GIF timing."""

import copy
import hashlib
import json
from pathlib import Path

from PIL import Image
from native_atlas import open_atlas

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


def validate_preservation(hashes, contract):
    expected_indices = set(range(60)) | set(range(180, 556))
    prior = contract['unchanged_cell_rgba_sha256']
    assert {int(index) for index in prior} == expected_indices
    assert contract['previous_version'] == '2.1.0'
    assert contract['previous_commit'] == 'b544c8caca7c9a4f84cd1e2bb8b22435b3aa39d4'
    for index, expected in prior.items():
        assert hashes[int(index)] == expected, index


def color_counts(frame):
    green = blue = pink = 0
    for r, g, b, a in frame.getdata():
        if a <= 128:
            continue
        green += g > 140 and r < 100 and b < 180
        blue += b > 150 and b > r * 1.5 and g > 50 and r < 80
        pink += r > 180 and g < 100 and b > 30
    return {'green': green, 'blue': blue, 'pink': pink}


def verify_native():
    release = json.loads((ROOT / 'release.json').read_text())
    assert release['version'] == '2.2.0'
    assert (release['format'], release['installFolder'], release['manifest'], release['atlas']) == (
        'codex-desktop-custom-tracks', 'capri', 'capri/pet.json', 'capri/spritesheet.webp')
    assert release['actionStates'] == STATES
    assert (release['framesPerAction'], release['configuredFps'], release['cycleMs']) == (60, 60, 1000)
    assert release['gazeCells'] == list(range(540, 556))
    assert release['gazePointerMappingVerified'] is False
    assert release['bodyColorsCorrected'] is True and release['gazeColorsCorrected'] is True
    assert release['lightningStates'] == ['running-right', 'running-left']
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
            allowed = {'self-lightning', 'electric-bridge-v2'} if state == 'running-right' else {state}
            if state == 'idle':
                allowed.add('border-repair')
            assert cell['asset'] in allowed
            assert cell['scale'] > 0 and isinstance(cell['source_index'], int)
    hashes = []
    measurements = {state: [] for state in release['lightningStates']}
    with open_atlas(path) as atlas:
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
                if 60 <= index < 180:
                    state = 'running-right' if index < 120 else 'running-left'
                    measurements[state].append(color_counts(cell))
    contract = json.loads((ROOT / 'qa/lightning-integration.json').read_text())
    assert contract['version'] == release['version']
    assert digest(ROOT / 'capri/pet.json') == contract['unchanged_manifest_sha256']
    validate_preservation(hashes, contract)
    invalid = hashes.copy()
    invalid[0] = '0' * 64
    try:
        validate_preservation(invalid, contract)
    except AssertionError:
        preservation_negative = 'rejected'
    else:
        raise AssertionError('Changed unrelated cell accepted')
    for state, colors in measurements.items():
        red = [i for i, item in enumerate(colors) if item['green'] < 2 and item['blue'] < 2 and item['pink'] > 1000]
        assert red == contract['phases'][state]['full_red_frames'] and len(red) >= 6
        assert all(colors[i]['green'] >= 20 and colors[i]['blue'] >= 5 for i in [0, 59])
    assert len(set(hashes[:540])) == 540 and len(set(hashes[540:])) == 16
    for position, state in enumerate(STATES):
        assert len(set(hashes[position * 60:(position + 1) * 60])) == 60, state

    gifs = []
    for name in STATES + ['all-actions', 'gaze', 'lightning-directions']:
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
    assert {item['file'] for item in browser['gifs']} == {
        f'media/60fps/{name}.gif' for name in ['all-actions', 'gaze', 'running-left', 'running-right', 'lightning-directions']}
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
            'unchanged_other_occupied_cells': 436, 'lightning_states': release['lightningStates'],
            'unrelated_cell_negative_control': preservation_negative,
            'unused_cells_transparent': 4, 'negative_controls': negative, 'gifs': gifs,
            'native_fps_measured': False, 'pointer_mapping_verified': False,
            'cli_256_cell_contract_compatible': False}


if __name__ == '__main__':
    print(json.dumps(verify_native(), indent=2))
