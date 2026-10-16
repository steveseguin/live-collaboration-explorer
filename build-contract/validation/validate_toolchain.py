"""Exercise external tooling end-to-end using synthetic fixtures; never accepts the product."""
import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from contract_tools import HERE, read_json, read_contract, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    parser.add_argument('--ffprobe', default=shutil.which('ffprobe'))
    args = parser.parse_args()
    if not args.ffmpeg or not args.ffprobe:
        parser.error('Provide trusted installed --ffmpeg and --ffprobe paths.')
    output = HERE / 'runs' / ('toolchain-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    output.mkdir(parents=True, exist_ok=False)
    checks = []
    env = os.environ.copy()
    env.pop('COHOST_ACCEPTANCE_CONFIG', None)
    env['COHOST_ACCEPTANCE_RUN'] = str(output / 'browser-no-target')
    python = os.sys.executable
    def run(name, command, expected=0, selected_env=None):
        completed = subprocess.run(command, cwd=HERE, env=selected_env or env,
                                   capture_output=True, text=True, encoding='utf-8', errors='replace')
        (output / f'{name}.stdout.txt').write_text(completed.stdout, encoding='utf-8')
        (output / f'{name}.stderr.txt').write_text(completed.stderr, encoding='utf-8')
        passed = completed.returncode == expected
        checks.append({'name': name, 'passed': passed, 'actualExit': completed.returncode, 'expectedExit': expected})
        if not passed:
            raise RuntimeError(f'{name} failed. Inspect private logs in {output}')
        return completed
    try:
        run('contract-consistency', [python, 'verify_contract.py'])
        npm = shutil.which('npm.cmd') if os.name == 'nt' else shutil.which('npm')
        if not npm: raise RuntimeError('npm is required to discover/validate the external browser harness.')
        listed = run('browser-discovery', [npm, 'run', 'list'])
        if '8 tests' not in listed.stdout:
            raise RuntimeError('Expected exactly eight browser cases in Playwright discovery.')
        # Deliberately no SUT config: every case must fail before opening a browser.
        run('missing-target-fails-closed', [npm, 'run', 'test:browser'], expected=1)
        browser = read_json(output / 'browser-no-target/browser-results.json')
        if len(browser['results']) != 8 or any(r['status'] == 'passed' for r in browser['results']):
            raise RuntimeError('Missing-target run unexpectedly passed or omitted browser cases.')
        run('empty-ledger-init', [python, 'completion.py', 'init', '--out', str(output / 'empty-ledger.json')])
        rejected = run('empty-ledger-rejected', [python, 'completion.py', 'check', str(output / 'empty-ledger.json')], expected=1)
        if json.loads(rejected.stdout)['accepted']:
            raise RuntimeError('Empty ledger was falsely accepted.')
        fake = read_json(output / 'empty-ledger.json')
        for record in fake['results']:
            record.update(status='passed', observations='Negative synthetic gate fixture; not product evidence.', environment='local')
        (output / 'no-evidence-ledger.json').write_text(json.dumps(fake), encoding='utf-8')
        rejected = run('passed-labels-without-evidence-rejected', [python, 'completion.py', 'check', str(output / 'no-evidence-ledger.json')], expected=1)
        if json.loads(rejected.stdout)['accepted']:
            raise RuntimeError('Self-declared passed labels were falsely accepted.')
        def negative(name, mutate, expected_error):
            candidate = json.loads(json.dumps(fake))
            mutate(candidate)
            path = output / (name + '.json')
            path.write_text(json.dumps(candidate), encoding='utf-8')
            checked = run(name, [python, 'completion.py', 'check', str(path)], expected=1)
            report = json.loads(checked.stdout)
            if report['accepted'] or not any(expected_error in message for message in report['errors']):
                raise RuntimeError(f'{name} did not reject its specific invalid evidence condition.')
        negative('stale-contract-rejected', lambda data: data.update(contractSha256='0' * 64),
                 'Contract SHA-256 mismatch')
        negative('escaped-artifact-rejected', lambda data: data['results'][0].update(evidence=[
            {'kind': 'screenshot', 'path': '../outside-ledger.png', 'sha256': '0' * 64}]),
            'Artifact escapes ledger root')
        artifact_path = output / 'negative-only-artifact.txt'
        artifact_path.write_text('Synthetic invalid-evidence fixture; not product evidence.', encoding='utf-8')
        negative('tampered-artifact-rejected', lambda data: data['results'][0].update(evidence=[
            {'kind': 'screenshot', 'path': artifact_path.name, 'sha256': '0' * 64}]),
            'Artifact SHA-256 mismatch')
        self_check = output / 'negative-only-measurement.json'
        self_check.write_text(json.dumps({'tool': 'negative-fixture', 'purpose': 'tool-self-check',
            'metrics': {'probe': 1}}), encoding='utf-8')
        negative('self-check-evidence-rejected', lambda data: data['results'][0].update(evidence=[
            {'kind': 'diagnostic-export', 'path': self_check.name, 'sha256': sha256(self_check)}]),
            'invalid or self-check-only measurement report')
        native = output / 'negative-only-skipped-browser.json'
        native.write_text(json.dumps({'suites': [{'specs': [{'title': 'T001 skipped fixture',
            'tests': [{'expectedStatus': 'passed', 'results': [{'status': 'skipped'}]}]}]}]}), encoding='utf-8')
        negative('skipped-native-browser-rejected', lambda data: data['results'][0].update(evidence=[
            {'kind': 'playwright-json', 'path': native.name, 'sha256': sha256(native)}]),
            'native Playwright case is missing/skipped/failed')
        run('generate-media-inputs', [python, 'generate_fixtures.py', '--ffmpeg', args.ffmpeg, '--force'])
        fixtures = HERE / 'fixtures-generated'
        host = output / 'synthetic-host-only.mp4'
        both = output / 'synthetic-host-and-guest.mp4'
        run('encode-synthetic-host', [args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(fixtures / 'host.y4m'), '-i', str(fixtures / 'host.wav'),
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k', '-t', '2', '-shortest', str(host)])
        run('encode-synthetic-both', [args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(fixtures / 'host.y4m'), '-i', str(fixtures / 'guest.y4m'),
            '-i', str(fixtures / 'host.wav'), '-i', str(fixtures / 'guest.wav'),
            '-filter_complex', '[0:v][1:v]hstack=inputs=2[v];[2:a][3:a]amix=inputs=2:normalize=0[a]',
            '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-t', '2', '-shortest', str(both)])
        for recording, name in [(host, 'host-only'), (both, 'both')]:
            run(f'analyze-{name}', [python, 'analyze_media.py', str(recording), '--ffmpeg', args.ffmpeg,
                '--ffprobe', args.ffprobe, '--start', '0.3', '--duration', '1.2', '--purpose', 'tool-self-check',
                '--out', str(output / f'{name}-analysis.json')])
        one, two = (read_json(output / name)['metrics'] for name in ('host-only-analysis.json', 'both-analysis.json'))
        if not (one['hostRedMinFraction'] > .5 and one['guestBlueMaxFraction'] < .001
                and one['hostToneMinDbfs'] > -35 and one['guestToneMaxDbfs'] < -55
                and two['hostRedMinFraction'] > .2 and two['guestBlueMinFraction'] > .2
                and two['hostToneMinDbfs'] > -35 and two['guestToneMinDbfs'] > -35):
            raise RuntimeError('Media oracle did not distinguish known synthetic presence/absence.')
        checks.append({'name': 'synthetic-source-identity-and-tone-roundtrip', 'passed': True})
        summary = {'toolchainValidated': True, 'productAccepted': False,
                   'requiredProductVariants': sum(len(t['variants']) for t in read_contract()['tests']),
                   'productVariantsPassed': 0, 'outputDirectory': str(output), 'checks': checks,
                   'note': 'Synthetic tooling/CLI checks only. Missing-target browser runs intentionally fail; no host application server or feature is tested.'}
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        summary = {'toolchainValidated': False, 'productAccepted': False, 'checks': checks, 'error': str(error), 'outputDirectory': str(output)}
    (output / 'toolchain-summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))
    return 0 if summary['toolchainValidated'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
