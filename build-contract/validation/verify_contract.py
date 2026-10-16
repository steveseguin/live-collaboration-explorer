"""Verify package consistency and traceability; this does not accept the product."""
import json
import re
from urllib.parse import unquote
from contract_tools import HERE, read_contract, sha256, CONTRACT


def main():
    contract = read_contract()
    errors = []
    requirements, tests = contract['requirements'], contract['tests']
    req_ids, test_ids = [r['id'] for r in requirements], [t['id'] for t in tests]
    if len(req_ids) != len(set(req_ids)) or len(test_ids) != len(set(test_ids)):
        errors.append('Duplicate requirement/test IDs.')
    for req in requirements:
        if not req.get('shall') or not req.get('basis') or not req.get('tests'):
            errors.append(f"Incomplete requirement {req['id']}")
        for test_id in req['tests']:
            if test_id not in test_ids:
                errors.append(f"Unknown test {test_id} on {req['id']}")
    browser_ids = []
    for test in tests:
        if not test['steps'] or not test['expected'] or not test['evidenceKinds']:
            errors.append(f"Incomplete scenario {test['id']}")
        expected = sorted(r['id'] for r in requirements if test['id'] in r['tests'])
        if sorted(test['requirements']) != expected or not expected:
            errors.append(f"Incorrect/orphan traceability on {test['id']}")
        if len(test['variants']) != len(set(test['variants'])) or not test['variants']:
            errors.append(f"Invalid variants on {test['id']}")
        for rule in test['metrics']:
            if rule['op'] not in ('<=', '>=', '==', 'in'):
                errors.append(f"Invalid metric operator on {test['id']}")
            if any(v not in test['variants'] for v in rule.get('variants', [])):
                errors.append(f"Invalid metric variant on {test['id']}")
        if test['method'] == 'browser':
            browser_ids.append(test['id'])
    suite = (HERE / 'browser/studio.spec.mjs').read_text(encoding='utf-8')
    actual_ids = re.findall(r"test\('?(T\d{3})\b", suite)
    if sorted(actual_ids) != sorted(browser_ids):
        errors.append(f'Browser suite/catalog mismatch: {actual_ids} versus {browser_ids}')
    package = HERE.parent
    documents = ['README.md', 'prd.md', 'trd.md', 'decisions-and-assumptions.md',
                 'integration-map.md', 'pseudocode.md', 'implementation-plan.md',
                 'requirements.md', 'acceptance-tests.md', 'evidence-and-completion.md',
                 'review-record.md', 'review-findings.md', 'validation/README.md']
    for name in documents:
        path = package / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f'Missing required document {name}')
            continue
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', path.read_text(encoding='utf-8')):
            if target.startswith(('https://', 'http://', 'mailto:', '#')):
                continue
            relative = unquote(target.strip('<>').split('#', 1)[0])
            if not (path.parent / relative).exists():
                errors.append(f'Broken local link in {name}: {target}')
    for name in ('requirements.md', 'acceptance-tests.md'):
        text = (package / name).read_text(encoding='utf-8')
        expected_ids = req_ids if name == 'requirements.md' else test_ids
        if any(i not in text for i in expected_ids):
            errors.append(f'Incomplete generated document {name}')
    for folder in (package, HERE):
        sitemap = (folder / 'README.md').read_text(encoding='utf-8')
        targets = {target.split('#', 1)[0] for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', sitemap)}
        for page in folder.glob('*.md'):
            if page.name != 'README.md' and page.name not in targets:
                errors.append(f'Missing package sitemap entry: {page.relative_to(package)}')
    print(json.dumps({'packageValid': not errors, 'productAccepted': False,
                      'requirements': len(requirements), 'scenarios': len(tests),
                      'requiredVariants': sum(len(t['variants']) for t in tests),
                      'suppliedBrowserCases': len(browser_ids),
                      'contractSha256': sha256(CONTRACT), 'errors': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
