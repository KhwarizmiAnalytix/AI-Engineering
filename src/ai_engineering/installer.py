"""Copy managed instructions into another project without overwriting native policy files."""
import argparse
import hashlib
import json
from importlib import resources
from pathlib import Path
import shutil

PKG_ROOT = resources.files('ai_engineering')
MARKER = '.ai-engineering-managed.json'


def checksum(data):
    return hashlib.sha256(data).hexdigest()


def build_arg_parser():
    ap = argparse.ArgumentParser(prog='ai-engineering install')
    ap.add_argument('--project', required=True, type=Path)
    ap.add_argument('--profile', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true', help='Update installer-managed files; back up local modifications')
    ap.add_argument('--entrypoints', action='store_true', help='Append reference to existing CLAUDE.md and AGENTS.md, or create when absent')
    return ap


def main(argv=None):
    run(build_arg_parser().parse_args(argv))


def run(args):
    profiles = json.loads(PKG_ROOT.joinpath('profiles/profiles.json').read_text())
    if args.profile not in profiles:
        raise SystemExit('Unknown profile: ' + args.profile)
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        raise SystemExit('Project does not exist: ' + str(project))
    cfg = profiles[args.profile]
    desired = {}
    for rule in cfg['rules']:
        data = PKG_ROOT.joinpath(f'rules/{rule}.md').read_text()
        desired[f'.claude/rules/ai-engineering-{rule}.md'] = data
        desired[f'.cursor/rules/ai-engineering-{rule}.mdc'] = '---\ndescription: AI-Engineering shared ' + rule + ' guidance\nalwaysApply: true\n---\n\n' + data
    for skill in cfg['skills']:
        data = PKG_ROOT.joinpath(f'skills/{skill}/SKILL.md').read_text()
        desired[f'.claude/skills/ai-engineering-{skill}/SKILL.md'] = data
        desired[f'.cursor/skills/ai-engineering-{skill}/SKILL.md'] = data
    desired['AI_ENGINEERING.md'] = (
        '# AI Engineering guidance\n\nProfile: ' + args.profile + '\n\n'
        + 'Check project-local `CLAUDE.md`, `AGENTS.md`, public headers and CI first. Shared rules are under `.claude/rules/ai-engineering-*` and `.cursor/rules/ai-engineering-*`; relevant skills live in `.claude/skills/ai-engineering-*` and `.cursor/skills/ai-engineering-*`.\n\n'
        + PKG_ROOT.joinpath(f'profiles/{args.profile}.md').read_text()
    )
    manifest_path = project / MARKER
    prior = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
    installed = {}
    for rel, content in sorted(desired.items()):
        target = project / rel
        data = content.encode()
        if target.exists():
            existing = target.read_bytes()
            if existing == data:
                print('OK    ', rel)
                installed[rel] = checksum(data)
                continue
            if not args.force or rel not in prior:
                print('SKIP  ', rel, '(existing file; use --force only for managed targets)')
                continue
            if checksum(existing) != prior[rel]:
                print('BACKUP', rel)
                if not args.dry_run:
                    shutil.copy2(target, target.with_name(target.name + '.ai-engineering.bak'))
        else:
            print('CREATE', rel)
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        installed[rel] = checksum(data)
    if args.entrypoints:
        block = '\n<!-- ai-engineering -->\nRead AI_ENGINEERING.md and apply it only where project-local rules are silent.\n<!-- /ai-engineering -->\n'
        for fn in ['CLAUDE.md', 'AGENTS.md']:
            path = project / fn
            existing = path.read_text() if path.exists() else ''
            if '<!-- ai-engineering -->' not in existing:
                print('APPEND', fn)
                if not args.dry_run:
                    path.write_text(existing + block)
    if not args.dry_run:
        # Preserve prior hashes for skipped paths so a later force can still safely update them.
        prior.update(installed)
        manifest_path.write_text(json.dumps(prior, indent=2, sort_keys=True) + '\n')
    print('Dry run; no files written.' if args.dry_run else 'Installed managed guidance.')


def list_profiles():
    profiles = json.loads(PKG_ROOT.joinpath('profiles/profiles.json').read_text())
    for name in sorted(profiles):
        print(name)


if __name__ == '__main__':
    main()
