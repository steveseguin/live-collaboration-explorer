"""Read-only snapshot of nonignored host application working files; output must be outside host application."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git(root, *args):
    return subprocess.check_output([
        'git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
        '-c', 'core.untrackedCache=false', '-C', str(root), *args
    ])


def snapshot(root, tracked_only=False, prefixes=None):
    listing = ['ls-files', '--cached', '--exclude-standard', '-z']
    if not tracked_only:
        listing.append('--others')
    names = sorted(set(git(root, *listing).decode('utf-8').split('\0')) - {''})
    if prefixes:
        names = [name for name in names if any(name.startswith(prefix) for prefix in prefixes)]
    files = {}
    for name in names:
        path = root / name
        try:
            if path.is_symlink():
                files[name] = {'symlink': str(path.readlink())}
            elif path.is_file():
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
                files[name] = {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}
            else:
                files[name] = {'missing': True}
        except OSError as error:
            files[name] = {'unreadable': type(error).__name__}
    return {'schemaVersion': 1, 'createdAt': datetime.now(timezone.utc).isoformat(),
            'head': git(root, 'rev-parse', 'HEAD').decode().strip(),
            'branch': git(root, 'branch', '--show-current').decode().strip(),
            'scope': {'trackedOnly': tracked_only, 'prefixes': prefixes or [],
                      'excludes': 'Git metadata and ignored untracked files'},
            'files': files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--compare', type=Path)
    parser.add_argument('--tracked-only', action='store_true')
    parser.add_argument('--prefix', action='append', default=[])
    args = parser.parse_args()
    root, out = args.source.resolve(), args.out.resolve()
    if out.is_relative_to(root):
        parser.error('Output must be outside the inspected source checkout.')
    data = snapshot(root, args.tracked_only, args.prefix)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    if args.compare:
        old = json.loads(args.compare.read_text(encoding='utf-8'))
        changed = sorted(name for name in set(old['files']) | set(data['files'])
                         if old['files'].get(name) != data['files'].get(name))
        unknown = sorted(name for name, item in data['files'].items() if 'unreadable' in item)
        same = (not changed and old['head'] == data['head'] and old['branch'] == data['branch']
                and old['scope'] == data['scope'])
        print(json.dumps({'accessibleFilesUnchanged': same, 'fullyVerified': same and not unknown,
                          'unreadableFiles': unknown, 'filesCompared': len(data['files']),
                          'headUnchanged': old['head'] == data['head'],
                          'branchUnchanged': old['branch'] == data['branch'],
                          'changedFiles': changed[:100]}))
        return (2 if unknown else 0) if same else 1
    print(json.dumps({'snapshotWritten': str(out), 'files': len(data['files']), 'head': data['head'],
                      'unreadableFiles': [name for name, item in data['files'].items() if 'unreadable' in item]}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
