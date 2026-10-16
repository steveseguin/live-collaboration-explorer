"""Shared read/validation helpers for the external acceptance tools."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = HERE.parent / 'contract.json'
RUNS = HERE / 'runs'


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    def reject_constant(value):
        raise ValueError(f'Invalid JSON numeric constant: {value}')
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=reject_constant)


def read_contract():
    return read_json(CONTRACT)


def private_output(path):
    path = Path(path).resolve()
    if not path.is_relative_to(RUNS.resolve()):
        raise ValueError(f'Write outputs only inside {RUNS}; never inside host application.')
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def artifact(root, entry):
    raw = entry.get('path')
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        raise ValueError('Artifact paths must be nonempty paths relative to the ledger directory.')
    path = (root / raw).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Artifact escapes ledger root: {raw}')
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f'Missing/empty artifact: {raw}')
    if sha256(path) != entry.get('sha256'):
        raise ValueError(f'Artifact SHA-256 mismatch: {raw}')
    return path


def metric_passes(actual, rule):
    expected, operator = rule['value'], rule['op']
    if operator in ('<=', '>='):
        if isinstance(actual, bool) or not isinstance(actual, (int, float)) or not math.isfinite(actual):
            return False
        return actual <= expected if operator == '<=' else actual >= expected
    if operator == '==':
        if isinstance(expected, bool) and not isinstance(actual, bool):
            return False
        if isinstance(expected, (int, float)) and not isinstance(expected, bool) and isinstance(actual, bool):
            return False
        return actual == expected
    if operator == 'in':
        return actual in expected
    return False
