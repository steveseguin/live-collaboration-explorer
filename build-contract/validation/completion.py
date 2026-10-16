"""Create/import/check revision-bound acceptance evidence; fail closed on incomplete results."""
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from contract_tools import CONTRACT, artifact, metric_passes, private_output, read_contract, read_json, sha256


def write_json(path, data):
    private_output(path).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def initialize(out):
    contract = read_contract()
    if Path(out).exists():
        raise ValueError('Refusing to overwrite an existing ledger. Choose a new run directory.')
    data = {'schemaVersion': 1, 'contractVersion': contract['version'],
            'contractSha256': sha256(CONTRACT),
            'run': {'implementationRevision': '', 'engineRevision': '',
                    'environmentKind': '', 'executedBy': '', 'startedAt': '', 'finishedAt': '',
                    'browserVersions': {}, 'deviceRecords': [], 'fixtureDescription': ''},
            'results': [{'testId': test['id'], 'variant': variant, 'status': 'not_run',
                         'environment': '', 'observations': '', 'metrics': {}, 'evidence': []}
                        for test in contract['tests'] for variant in test['variants']]}
    write_json(out, data)
    print(json.dumps({'ledgerCreated': str(out), 'results': len(data['results']), 'accepted': False}))


def native_outcomes(data):
    if data.get('errors'):
        return {}
    outcomes = {}
    def visit(suites):
        for suite in suites:
            for spec in suite.get('specs', []):
                match = re.match(r'(T\d{3})\b', spec.get('title', ''))
                if match:
                    attempts = [r for t in spec.get('tests', []) for r in t.get('results', [])]
                    success = bool(attempts) and all(r.get('status') == 'passed' for r in attempts)
                    success = success and all(t.get('expectedStatus') == 'passed' for t in spec.get('tests', []))
                    outcomes.setdefault(match.group(1), []).append(success)
            visit(suite.get('suites', []))
    visit(data.get('suites', []))
    return {key: all(value) for key, value in outcomes.items()}


def import_browser(ledger_path, report_path):
    ledger_path = private_output(ledger_path)
    data, report = read_json(ledger_path), read_json(report_path)
    contract = read_contract()
    for key in ('implementationRevision', 'engineRevision'):
        if not data['run'].get(key) or data['run'][key] != report.get(key):
            raise ValueError(f'Browser report {key} does not match ledger.')
    if report.get('contractSha256') != sha256(CONTRACT) or data.get('contractSha256') != sha256(CONTRACT):
        raise ValueError('Contract hash mismatch; rerun against the current contract.')
    native_path = Path(report['playwrightReportPath']).resolve()
    native_data = read_json(native_path)
    native_metadata = native_data.get('config', {}).get('metadata', {})
    if any(native_metadata.get(key) != report.get(key) for key in ('implementationRevision', 'engineRevision', 'contractSha256')):
        raise ValueError('Native Playwright report metadata does not match the acceptance report.')
    native = native_outcomes(native_data)
    allowed = {t['id'] for t in contract['tests'] if t['method'] == 'browser'}
    dest = ledger_path.parent / 'browser-evidence'
    dest.mkdir(exist_ok=True)
    raw_dest = dest / 'playwright.json'
    shutil.copy2(native_path, raw_dest)
    imported = []
    for item in report.get('results', []):
        test_id = item['testId']
        if test_id not in allowed:
            raise ValueError(f'Cannot import non-browser case {test_id}')
        entry = next(r for r in data['results'] if r['testId'] == test_id and r['variant'] == 'default')
        entry.update(status='passed' if item['status'] == 'passed' and native.get(test_id) else 'failed',
                     environment=report.get('environmentKind', ''), observations='Imported from actual Playwright run; see attached raw report.',
                     evidence=[{'kind': 'playwright-json', 'path': str(raw_dest.relative_to(ledger_path.parent)), 'sha256': sha256(raw_dest)}])
        for n, image in enumerate(item.get('screenshots', [])):
            source = Path(image)
            if source.is_file():
                target = dest / f'{test_id}-{n}.png'
                shutil.copy2(source, target)
                entry['evidence'].append({'kind': 'screenshot', 'path': str(target.relative_to(ledger_path.parent)), 'sha256': sha256(target)})
        imported.append(test_id)
    write_json(ledger_path, data)
    print(json.dumps({'imported': imported, 'accepted': False, 'note': 'Run check for all mandatory variants/evidence.'}))


def check(path):
    data, contract = read_json(path), read_contract()
    errors, root = [], Path(path).resolve().parent
    if data.get('schemaVersion') != 1 or data.get('contractVersion') != contract['version']:
        errors.append('Ledger/contract schema or version mismatch.')
    if data.get('contractSha256') != sha256(CONTRACT):
        errors.append('Contract SHA-256 mismatch.')
    run = data.get('run', {})
    for key in ('implementationRevision', 'engineRevision'):
        if not re.fullmatch(r'[0-9a-fA-F]{7,64}', run.get(key, '')):
            errors.append(f'Missing/unpinned {key}.')
    if run.get('environmentKind') != 'local-and-qa':
        errors.append('Full profile requires local-and-qa evidence, including real QA buyer playback.')
    for key in ('executedBy', 'fixtureDescription'):
        value = run.get(key, '')
        if not isinstance(value, str) or len(value.strip()) < 3 or '<' in value or 'TODO' in value:
            errors.append(f'Missing/unresolved run.{key}.')
    try:
        start, finish = (datetime.fromisoformat(run.get(k, '').replace('Z', '+00:00')) for k in ('startedAt', 'finishedAt'))
        if start.tzinfo is None or finish.tzinfo is None or finish < start:
            raise ValueError('Bad timestamps')
    except (TypeError, ValueError):
        errors.append('Run requires valid ordered timezone-aware start/finish timestamps.')
    browsers = run.get('browserVersions', {})
    if not all(isinstance(browsers.get(key), str) and browsers[key].strip() for key in ('hostChrome', 'hostEdge')):
        errors.append('Missing actual host Chrome/Edge versions.')
    if not isinstance(run.get('deviceRecords'), list) or len(run['deviceRecords']) < 2:
        errors.append('Missing physical Android/iPhone run records.')
    results = {}
    for result in data.get('results', []):
        key = (result.get('testId'), result.get('variant'))
        if key in results:
            errors.append(f'Duplicate result {key}.')
        results[key] = result
    expected = {(test['id'], variant) for test in contract['tests'] for variant in test['variants']}
    if set(results) - expected:
        errors.append(f'Unrecognized results: {sorted(set(results) - expected)}')
    passed = set()
    for test in contract['tests']:
        for variant in test['variants']:
            key = (test['id'], variant)
            label, before = '/'.join(key), len(errors)
            result = results.get(key)
            if not result or result.get('status') != 'passed':
                errors.append(f"{label}: {result.get('status', 'missing') if result else 'missing'}")
                continue
            if result.get('environment') not in ('local', 'qa', 'physical-device'):
                errors.append(f'{label}: invalid/missing environment.')
            if test['method'] == 'real-device' and result.get('environment') != 'physical-device':
                errors.append(f'{label}: real-device evidence cannot use emulation.')
            if test['id'] == 'T036' and result.get('environment') != 'qa':
                errors.append(f'{label}: actual QA buyer evidence is required.')
            if not str(result.get('observations', '')).strip():
                errors.append(f'{label}: missing execution observations/interval references.')
            kinds, recordings, analysis, measurement_reports = set(), set(), [], []
            for entry in result.get('evidence', []):
                try:
                    evidence_path = artifact(root, entry)
                    kinds.add(entry.get('kind'))
                    if entry.get('kind') == 'receiver-recording':
                        recordings.add(entry['sha256'])
                    if entry.get('kind') == 'media-analysis':
                        analysis.append(read_json(evidence_path))
                    if entry.get('kind') in ('media-analysis', 'performance-report', 'timing-report',
                            'network-summary', 'diagnostic-export', 'event-timeline', 'service-log',
                            'device-record', 'build-manifest') and evidence_path.suffix.lower() == '.json':
                        measured = read_json(evidence_path)
                        if isinstance(measured.get('metrics'), dict):
                            measurement_reports.append((entry['kind'], measured))
                    if entry.get('kind') == 'playwright-json':
                        native = read_json(evidence_path)
                        metadata = native.get('config', {}).get('metadata', {})
                        if not native_outcomes(native).get(test['id']):
                            errors.append(f'{label}: native Playwright case is missing/skipped/failed.')
                        if any(metadata.get(key) != run.get(key) for key in ('implementationRevision', 'engineRevision')) or metadata.get('contractSha256') != sha256(CONTRACT):
                            errors.append(f'{label}: native Playwright revision/contract mismatch.')
                except (ValueError, OSError, json.JSONDecodeError) as error:
                    errors.append(f'{label}: {error}')
            missing = set(test['evidenceKinds']) - kinds
            if missing:
                errors.append(f'{label}: missing evidence kinds {sorted(missing)}')
            for report in analysis:
                if report.get('sourceSha256') not in recordings:
                    errors.append(f'{label}: media analysis is not bound to an attached receiver recording.')
                if not report.get('analysisWindow') or not report.get('tool') or not isinstance(report.get('metrics'), dict):
                    errors.append(f'{label}: incomplete media-analysis report.')
            for kind, report in measurement_reports:
                if not report.get('tool') or report.get('purpose') == 'tool-self-check':
                    errors.append(f'{label}: invalid or self-check-only measurement report.')
                if any(report.get(key) != run.get(key) for key in ('implementationRevision', 'engineRevision')) or report.get('contractSha256') != sha256(CONTRACT):
                    errors.append(f'{label}: measurement revision/contract mismatch.')
                if kind in ('media-analysis', 'performance-report', 'timing-report') and report.get('sourceSha256') not in recordings:
                    errors.append(f'{label}: independent measurement report is not bound to an attached receiver recording.')
            for rule in test['metrics']:
                if rule.get('variants') and variant not in rule['variants']:
                    continue
                actual = result.get('metrics', {}).get(rule['key'])
                if not metric_passes(actual, rule):
                    errors.append(f"{label}: {rule['key']}={actual!r}, requires {rule['op']} {rule['value']!r}")
                reports = [report for kind, report in measurement_reports
                           if rule['key'] in report.get('metrics', {})]
                if any(word in rule['key'] for word in ('Red', 'Blue', 'Tone')) or rule['key'] in ('width', 'height'):
                    reports = [report for kind, report in measurement_reports if kind == 'media-analysis'
                               and rule['key'] in report.get('metrics', {})]
                if not any(report['metrics'][rule['key']] == actual for report in reports):
                    errors.append(f"{label}: {rule['key']} is not backed by a matching attached measurement report.")
            if len(errors) == before:
                passed.add(key)
    covered = [r['id'] for r in contract['requirements'] if all(
        (test_id, variant) in passed for test_id in r['tests']
        for variant in next(t['variants'] for t in contract['tests'] if t['id'] == test_id))]
    print(json.dumps({'accepted': not errors, 'profile': contract['profile'],
                      'passingVariants': len(passed), 'requiredVariants': len(expected),
                      'satisfiedRequirements': len(covered), 'requiredRequirements': len(contract['requirements']),
                      'errors': errors, 'warning': 'Structural/evidence checks do not replace review of artifact truth.'}, indent=2))
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init'); init.add_argument('--out', type=Path, required=True)
    verify = sub.add_parser('check'); verify.add_argument('ledger', type=Path)
    imp = sub.add_parser('import-browser'); imp.add_argument('ledger', type=Path); imp.add_argument('report', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init': initialize(args.out); return 0
        if args.command == 'import-browser': import_browser(args.ledger, args.report); return 0
        return check(args.ledger)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({'accepted': False, 'error': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
