#!/usr/bin/env python3
"""Import a local Sweat Bench run into reproducible, text-only review evidence.

Reads original artifacts without modifying them. Never extracts model reasoning.
No network operations. Imported evidence is local-only until its contents are
reviewed for publication; excluding reasoning is not a secret scanner.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path

DIRECTORIES = {'lib', 'test', 'docs', 'config', 'priv'}
ROOT_FILES = {'mix.exs', 'mix.lock', 'TASK.md', 'README.md'}
EXCLUDED = {'deps', '_build', 'node_modules', 'db'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def eligible(path: Path) -> bool:
    parts = path.parts
    if any(part.startswith('.') or part in EXCLUDED for part in parts):
        return False
    if path.suffix.lower() in {'.db', '.sqlite', '.sqlite3'} or path.name.endswith(('-wal', '-shm')):
        return False
    return (len(parts) > 1 and parts[0] in DIRECTORIES) or (len(parts) == 1 and parts[0] in ROOT_FILES)


def capture_snapshot(root: Path, destination: Path) -> dict:
    if not root.is_dir():
        raise ValueError(f'Missing snapshot: {root}')
    files = {}
    for original in sorted(root.rglob('*')):
        relative = original.relative_to(root)
        if not original.is_file() or original.is_symlink() or not eligible(relative):
            continue
        data = original.read_bytes()
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if '\x00' in text:
            continue
        name = relative.as_posix()
        files[name] = {'text': text, 'sha256': digest(data), 'lines': len(text.splitlines())}
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    fingerprint = digest(''.join(f'{name}\0{file["sha256"]}\n' for name, file in sorted(files.items())).encode('utf-8'))
    return {'fingerprint': fingerprint, 'files': files}


def compare(base: int, head: int, snapshots: dict) -> dict:
    before = snapshots[str(base)]['files']
    after = snapshots[str(head)]['files']
    changed = []
    for path in sorted(before.keys() | after.keys()):
        a, b = before.get(path), after.get(path)
        if a and b and a['sha256'] == b['sha256']:
            continue
        old = a['text'].splitlines() if a else []
        new = b['text'].splitlines() if b else []
        matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
        added = removed = 0
        for tag, i, j, k, l in matcher.get_opcodes():
            if tag in ('replace', 'delete'):
                removed += j - i
            if tag in ('replace', 'insert'):
                added += l - k
        patch = '\n'.join(difflib.unified_diff(old, new, fromfile=f'milestone-{base}/{path}' if a else '/dev/null', tofile=f'milestone-{head}/{path}' if b else '/dev/null', lineterm=''))
        changed.append({'path': path, 'status': 'added' if not a else 'deleted' if not b else 'modified', 'added': added, 'removed': removed, 'diff': patch})
    return {'base': base, 'head': head, 'changed': changed,
            'sourceChangedCount': sum(c['path'].split('/')[0] in {'lib', 'config', 'priv'} or c['path'] in {'mix.exs', 'mix.lock'} for c in changed),
            'testChangedCount': sum(c['path'].startswith('test/') for c in changed),
            'docChangedCount': sum(c['path'].startswith('docs/') or c['path'] in {'TASK.md', 'README.md'} for c in changed)}


def author_handoff(log: Path) -> dict | None:
    if not log.is_file():
        return None
    final = None
    for line_number, line in enumerate(log.read_text().splitlines(), 1):
        record = json.loads(line)
        if record.get('type') != 'assistant':
            continue
        content = record.get('message', {}).get('content', [])
        if not isinstance(content, list):
            continue
        # Only public assistant text; never thinking/reasoning/tool_use content.
        text = '\n'.join(item['text'] for item in content if isinstance(item, dict) and item.get('type') == 'text' and isinstance(item.get('text'), str))
        if text.strip():
            final = {'text': text, 'source': str(log), 'line': line_number}
    return final


def build(run: Path, milestones: list[int], out: Path) -> dict:
    run, out = run.expanduser().resolve(), out.expanduser().resolve()
    if out == run or run in out.parents or out in run.parents:
        raise ValueError('Output must not overlap the source run directory')
    selected = sorted(set(milestones))
    if not selected or min(selected) < 2:
        raise ValueError('Select head milestones >= 2; each needs its predecessor snapshot')
    needed = sorted(set(selected) | {m - 1 for m in selected})
    bundle = {'schemaVersion': 1, 'runId': run.name, 'importedAt': datetime.now(timezone.utc).isoformat(), 'sourceRoot': f'sweatbench-run:{run.name}', 'milestones': {}, 'comparisons': {}, 'reports': {}, 'authorHandoffs': {}, 'evaluationLogs': {}}
    for m in needed:
        key = str(m)
        bundle['milestones'][key] = capture_snapshot(run / 'snapshots' / f'milestone-{m}', out / 'snapshots' / f'milestone-{m}')
        report = run / 'reports' / f'milestone-{m}.json'
        if report.is_file():
            bundle['reports'][key] = json.loads(report.read_text())
        evaluation_log = run / 'logs' / f'evaluate-{m}.log'
        if evaluation_log.is_file():
            bundle['evaluationLogs'][key] = evaluation_log.read_text()
    for m in selected:
        bundle['comparisons'][str(m)] = compare(m - 1, m, bundle['milestones'])
        handoff = author_handoff(run / 'logs' / f'agent-{m}.jsonl')
        if handoff:
            handoff['source'] = f'logs/agent-{m}.jsonl'
            bundle['authorHandoffs'][str(m)] = handoff
    out.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(bundle, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    (out / 'bundle.json').write_bytes(encoded)
    manifest = {'schemaVersion': 1, 'runId': bundle['runId'], 'importedAt': bundle['importedAt'], 'sourceRoot': bundle['sourceRoot'], 'bundleSha256': digest(encoded), 'localOnly': True,
                'snapshots': {m: {'fingerprint': snapshot['fingerprint'], 'fileCount': len(snapshot['files'])} for m, snapshot in bundle['milestones'].items()},
                'comparisons': {m: {k: v for k, v in comparison.items() if k != 'changed'} | {'changedFileCount': len(comparison['changed'])} for m, comparison in bundle['comparisons'].items()},
                'notes': ['Historical author handoffs are not independent reviews.', 'Evaluator reports are historical, not fresh executions.', 'Aggregate evaluator totals may include system checks.', 'Snapshot fingerprints cover only the imported text source selection, not full repositories.']}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--milestones', type=int, nargs='+', default=[3, 4])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.run, args.milestones, args.out), indent=2))


if __name__ == '__main__':
    main()
