"""Measure input color identities and tones in an independent program recording.

This is a partial media oracle, not proof of fps, source motion, A/V sync or device behavior.
"""
import argparse
import array
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from contract_tools import CONTRACT, private_output, sha256


def decode(command):
    return subprocess.check_output(command, stderr=subprocess.PIPE)


def tone_dbfs(samples, frequency, rate):
    # Exact 100 ms blocks contain whole 440/880 Hz periods. Projection returns RMS.
    n = len(samples)
    cosine = sum(value * math.cos(2 * math.pi * frequency * i / rate) for i, value in enumerate(samples))
    sine = sum(value * math.sin(2 * math.pi * frequency * i / rate) for i, value in enumerate(samples))
    rms = math.sqrt(2) * math.hypot(cosine, sine) / max(n, 1) / 32768
    return 20 * math.log10(max(rms, 1e-8))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recording', type=Path)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    parser.add_argument('--ffprobe', default=shutil.which('ffprobe'))
    parser.add_argument('--start', type=float, required=True)
    parser.add_argument('--duration', type=float, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--purpose', choices=['implementation', 'tool-self-check'], default='implementation')
    parser.add_argument('--implementation-revision', default='')
    parser.add_argument('--engine-revision', default='')
    args = parser.parse_args()
    if not args.ffmpeg or not args.ffprobe:
        parser.error('Provide installed trusted --ffmpeg and --ffprobe executables.')
    if not args.recording.is_file() or args.start < 0 or not 1 <= args.duration <= 120:
        parser.error('A recording and an explicit 1..120 second nonnegative analysis window are required.')
    if args.purpose == 'implementation' and not all(re.fullmatch(r'[a-fA-F0-9]{7,64}', value)
            for value in (args.implementation_revision, args.engine_revision)):
        parser.error('Implementation analysis requires pinned --implementation-revision and --engine-revision.')
    target = private_output(args.out)
    probe = json.loads(decode([args.ffprobe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(args.recording)]))
    video = next((s for s in probe['streams'] if s.get('codec_type') == 'video'), None)
    audio = next((s for s in probe['streams'] if s.get('codec_type') == 'audio'), None)
    if not video or not audio:
        parser.error('Media oracle requires both a real video and audio stream; missing audio is not evidence of correct gating.')
    common = [args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-ss', str(args.start), '-i', str(args.recording), '-t', str(args.duration)]
    # Decode to a bounded tiny image for identity occupancy; this sampling is NOT an fps metric.
    width, height = 96, 128
    raw = decode(common + ['-map', '0:v:0', '-vf', f'fps=5,scale={width}:{height}', '-an', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'])
    frame_size = width * height * 3
    if len(raw) < frame_size * 3 or len(raw) % frame_size:
        parser.error('Insufficient/invalid decoded video in the declared analysis interval.')
    fractions = []
    for start in range(0, len(raw), frame_size):
        frame, red, blue = raw[start:start + frame_size], 0, 0
        for i in range(0, frame_size, 3):
            r, g, b = frame[i:i + 3]
            red += r > 80 and r > 1.5 * g and r > 1.5 * b
            blue += b > 80 and b > 1.5 * r and b > 1.5 * g
        fractions.append((red / (width * height), blue / (width * height)))
    if len(fractions) / 5 < args.duration - 0.4:
        parser.error('Recording does not cover the requested video analysis duration.')
    pcm = decode(common + ['-map', '0:a:0', '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', 'pipe:1'])
    samples = array.array('h'); samples.frombytes(pcm)
    if sys.byteorder != 'little': samples.byteswap()
    block = 1600
    chunks = [samples[i:i + block] for i in range(0, len(samples) - block + 1, block)]
    if len(chunks) < 5: parser.error('Insufficient decoded audio for tone measurements.')
    if len(samples) / 16000 < args.duration - 0.2:
        parser.error('Recording does not cover the requested audio analysis duration.')
    levels = {frequency: [tone_dbfs(chunk, frequency, 16000) for chunk in chunks] for frequency in (440, 880)}
    metrics = {'width': video['width'], 'height': video['height'],
               'hostRedMinFraction': min(r for r, _ in fractions), 'hostRedMaxFraction': max(r for r, _ in fractions),
               'guestBlueMinFraction': min(b for _, b in fractions), 'guestBlueMaxFraction': max(b for _, b in fractions),
               'hostToneMinDbfs': min(levels[440]), 'hostToneMaxDbfs': max(levels[440]),
               'guestToneMinDbfs': min(levels[880]), 'guestToneMaxDbfs': max(levels[880]),
               'clippedSampleFraction': sum(abs(x) >= 32760 for x in samples) / max(1, len(samples))}
    report = {'schemaVersion': 1, 'tool': 'analyze_media.py/1.0.0',
              'purpose': args.purpose, 'implementationRevision': args.implementation_revision,
              'engineRevision': args.engine_revision, 'contractSha256': sha256(CONTRACT),
              'ffmpeg': subprocess.check_output([args.ffmpeg, '-version'], text=True).splitlines()[0],
              'sourceSha256': sha256(args.recording), 'analysisWindow': {'startSeconds': args.start, 'durationSeconds': args.duration},
              'videoIdentitySamples': len(fractions), 'audioWindows': len(chunks), 'metrics': metrics,
              'limits': 'Identity/tone occupancy only. Does not measure source freshness, fps, freezes, geometry, A/V sync, one-way delay, echo or physical devices.',
              'productAccepted': False}
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': str(target), 'metrics': metrics, 'productAccepted': False}, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())
