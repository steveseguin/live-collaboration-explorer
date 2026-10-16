"""Generate moving, distinguishable laboratory camera/audio inputs outside host application."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from contract_tools import HERE, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    parser.add_argument('--width', type=int, default=320)
    parser.add_argument('--height', type=int, default=240)
    parser.add_argument('--seconds', type=int, default=2)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error('Provide --ffmpeg with an installed trusted FFmpeg executable.')
    if args.width < 160 or args.height < 120 or args.width % 2 or args.height % 2 or not 1 <= args.seconds <= 30:
        parser.error('Use even dimensions >=160x120 and duration 1..30 seconds.')
    output = HERE / 'fixtures-generated'
    output.mkdir(exist_ok=True)
    metadata = {'tool': 'generate_fixtures.py/1.0.0', 'purpose': 'laboratory inputs, not physical-device evidence',
                'width': args.width, 'height': args.height, 'fps': 30, 'seconds': args.seconds, 'files': []}
    version = subprocess.check_output([args.ffmpeg, '-version'], text=True).splitlines()[0]
    metadata['ffmpeg'] = version
    for role, color, tone in [('host', 'red', 440), ('guest', 'blue', 880)]:
        video, audio = output / f'{role}.y4m', output / f'{role}.wav'
        if not args.force and (video.exists() or audio.exists()):
            parser.error('Fixture already exists; use --force only to replace generated fixtures.')
        subprocess.run([args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
            '-f', 'lavfi', '-i', f'testsrc2=size={args.width}x{args.height}:rate=30:duration={args.seconds}',
            '-vf', f'drawbox=x=0:y=0:w=iw:h=ih:color={color}@0.8:t=fill,format=yuv420p',
            '-an', '-f', 'yuv4mpegpipe', str(video)], check=True)
        subprocess.run([args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
            '-f', 'lavfi', '-i', f'sine=frequency={tone}:sample_rate=48000:duration={args.seconds}',
            '-c:a', 'pcm_s16le', '-ac', '1', str(audio)], check=True)
        metadata['files'].extend({'file': p.name, 'sha256': sha256(p), 'bytes': p.stat().st_size}
                                 for p in [video, audio])
    (output / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'fixturesGenerated': str(output), 'productAccepted': False, 'ffmpeg': version}))


if __name__ == '__main__':
    raise SystemExit(main())
