"""Read a large lossless atlas as cells without retaining a decoded full image."""
from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image


class AtlasCells:
    def __init__(self, raw, size):
        self.raw = raw
        self.size = size

    def crop(self, box):
        left, top, right, bottom = box
        width, height = self.size
        assert 0 <= left < right <= width and 0 <= top < bottom <= height
        rows = []
        for y in range(top, bottom):
            self.raw.seek((y * width + left) * 4)
            row = self.raw.read((right - left) * 4)
            assert len(row) == (right - left) * 4
            rows.append(row)
        return Image.frombytes('RGBA', (right - left, bottom - top), b''.join(rows))


@contextmanager
def open_atlas(path):
    """Decode one static lossless WebP with FFmpeg; clean temporary bytes on exit."""
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('Maintainer checks require FFmpeg/ffprobe on PATH and Python Pillow.')
    with path.open('rb') as encoded:
        header = encoded.read(12)
        assert header[:4] == b'RIFF' and header[8:] == b'WEBP'
        chunks = []
        while chunk := encoded.read(8):
            assert len(chunk) == 8
            kind, length = chunk[:4], int.from_bytes(chunk[4:], 'little')
            chunks.append(kind)
            encoded.seek(length + length % 2, 1)
        assert b'VP8L' in chunks and not {b'ANIM', b'ANMF', b'VP8 '} & set(chunks)
    metadata = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,codec_name', '-of', 'json', str(path)], timeout=30))
    assert len(metadata['streams']) == 1
    stream = metadata['streams'][0]
    assert stream['codec_name'] == 'webp'
    size = stream['width'], stream['height']
    assert size == (3072, 7280)
    with TemporaryDirectory(prefix='capri-atlas-') as directory:
        target = Path(directory) / 'atlas.rgba'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-threads', '1',
                        '-i', str(path), '-frames:v', '1', '-f', 'rawvideo',
                        '-pix_fmt', 'rgba', '-y', str(target)], check=True, timeout=60)
        assert target.stat().st_size == size[0] * size[1] * 4
        with target.open('rb') as raw:
            yield AtlasCells(raw, size)
