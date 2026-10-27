"""Register thin user-level integrations; policy remains in the Python package."""

import json
from pathlib import Path
import shutil

from ai_engineering import catalog
from ai_engineering.installer import checksum

MANIFEST = '.config/ai-engineering/managed.json'
CURSOR_RULE = '.config/ai-engineering/cursor-user-rule.md'
BOOTSTRAP = '''# Shared AI Engineering guidance

At the start of work in a repository, run `ai-engineering context --project .`
from that repository and read its output. Follow project-local instructions and
the existing API first; use the shared guidance where local policy is silent.
Load relevant task workflows with `ai-engineering skill <name>`.
If the command is unavailable, report that shared guidance could not be loaded.
'''


def desired_files(tool):
    # Cursor also discovers ~/.claude/skills, so "all" needs only one registration.
    skill_root = '.cursor/skills' if tool == 'cursor' else '.claude/skills'
    desired = {
        f'{skill_root}/ai-engineering/SKILL.md': (
            '---\nname: ai-engineering\ndescription: Load shared C++ engineering rules '
            'and project context before working in a repository.\n---\n\n' + BOOTSTRAP
        ),
    }
    for name in catalog.skill_names():
        desired[f'{skill_root}/ai-engineering-{name}/SKILL.md'] = (
            f'---\nname: ai-engineering-{name}\ndescription: '
            + json.dumps(catalog.skill_description(name)) + '\n---\n\n'
            + f'# Shared {name} workflow\n\n'
            + 'Read project-local instructions first. Run `ai-engineering context --project .` '
            + 'if shared context has not been loaded for this repository.\n\n'
            + f'Run `ai-engineering skill {name}` and read its output before performing '
            + 'this task. The installed Python package contains the full workflow; '
            + 'apply it only where local policy is silent.\n'
        )
    if tool in ('all', 'claude'):
        desired['.claude/rules/ai-engineering.md'] = BOOTSTRAP
    if tool in ('all', 'cursor'):
        desired[CURSOR_RULE] = BOOTSTRAP
    return desired


def load_manifest(home):
    path = home / MANIFEST
    if path.is_symlink():
        raise ValueError('Refusing symlink manifest: ' + str(path))
    prior = json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}
    if not isinstance(prior, dict):
        raise ValueError('Invalid managed manifest: expected an object')
    for rel, digest in prior.items():
        path = Path(rel)
        allowed_skill = (
            len(path.parts) == 4 and path.parts[0] in ('.claude', '.cursor')
            and path.parts[1] == 'skills'
            and (path.parts[2] == 'ai-engineering' or path.parts[2].startswith('ai-engineering-'))
            and path.parts[3] == 'SKILL.md'
        )
        if (not allowed_skill and rel not in (CURSOR_RULE, '.claude/rules/ai-engineering.md')) or '..' in path.parts:
            raise ValueError('Invalid managed path: ' + rel)
        if not isinstance(digest, str):
            raise ValueError('Invalid managed checksum: ' + rel)
    return prior


def backup_path(target):
    backup = target.with_name(target.name + '.ai-engineering.bak')
    index = 1
    while backup.exists() or backup.is_symlink():
        backup = target.with_name(target.name + f'.ai-engineering.bak.{index}')
        index += 1
    return backup


def setup(home, tool='all', dry_run=False, force=False):
    home = Path(home).expanduser().resolve()
    prior = load_manifest(home)
    conflicts = []
    for rel, content in sorted(desired_files(tool).items()):
        target = home / rel
        data = content.encode('utf-8')
        if target.is_symlink() or (target.exists() and not target.is_file()):
            print('SKIP  ', rel, '(symlink or non-file)')
            conflicts.append(rel)
            continue
        if target.exists():
            existing = target.read_bytes()
            if existing == data:
                print('OK    ', rel)
                prior[rel] = checksum(data)
                continue
            if rel not in prior or (checksum(existing) != prior[rel] and not force):
                print('SKIP  ', rel, '(unmanaged or locally modified)')
                conflicts.append(rel)
                continue
            if checksum(existing) != prior[rel]:
                backup = backup_path(target)
                print('BACKUP', backup.relative_to(home))
                if not dry_run:
                    shutil.copy2(target, backup)
            print('UPDATE', rel)
        else:
            print('CREATE', rel)
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        prior[rel] = checksum(data)
    if not dry_run:
        manifest = home / MANIFEST
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(prior, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('Dry run; no files written.' if dry_run else 'Registered user-level guidance. Start a new agent session.')
    if tool in ('all', 'cursor'):
        print('\nOne-time Cursor setup: paste the following into Customize > Rules > User Rules')
        print(f'(also saved at {home / CURSOR_RULE} when not using --dry-run):\n')
        print(BOOTSTRAP)
    return 1 if conflicts else 0


def uninstall(home, dry_run=False):
    home = Path(home).expanduser().resolve()
    prior = load_manifest(home)
    remaining = dict(prior)
    for rel, digest in sorted(prior.items()):
        target = home / rel
        if target.is_symlink() or (target.exists() and not target.is_file()):
            print('KEEP  ', rel, '(symlink or non-file)')
            continue
        if not target.exists():
            remaining.pop(rel)
            continue
        if checksum(target.read_bytes()) != digest:
            print('KEEP  ', rel, '(locally modified)')
            continue
        print('REMOVE', rel)
        if not dry_run:
            target.unlink()
        remaining.pop(rel)
    if not dry_run:
        manifest = home / MANIFEST
        if remaining:
            manifest.write_text(json.dumps(remaining, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        elif manifest.exists():
            manifest.unlink()
    print('Dry run; no files written.' if dry_run else 'Removed unmodified user-level registrations.')
    print('Remove the AI Engineering User Rule from Cursor Settings if you added it.')
    return 1 if remaining else 0
