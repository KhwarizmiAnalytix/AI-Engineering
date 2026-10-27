"""Read guidance from the installed package without creating project files."""

import json
from importlib import resources
from pathlib import Path


def read(relative):
    return resources.files('ai_engineering').joinpath(relative).read_text(encoding='utf-8')


def profiles():
    return json.loads(read('profiles/profiles.json'))


def skill_names():
    return sorted(
        item.name for item in resources.files('ai_engineering').joinpath('skills').iterdir()
        if item.is_dir() and item.joinpath('SKILL.md').is_file()
    )


def skill(name):
    if name not in skill_names():
        raise ValueError('Unknown skill: ' + name)
    return read(f'skills/{name}/SKILL.md')


def skill_description(name):
    for line in skill(name).splitlines():
        if line.startswith('description: '):
            return line.removeprefix('description: ')
    raise ValueError('Missing skill description: ' + name)


def project_root(project):
    path = Path(project).expanduser().resolve()
    if not path.is_dir():
        raise ValueError('Project does not exist: ' + str(path))
    known = {name.casefold() for name in profiles()}
    for candidate in (path, *path.parents):
        if (candidate / '.git').exists() or (candidate / 'pyproject.toml').is_file():
            return candidate
        if candidate.name.casefold() in known:
            return candidate
    return path


def context(project, profile=None):
    root = project_root(project)
    available = profiles()
    if profile is None:
        profile = next((name for name in available if name.casefold() == root.name.casefold()), None)
    elif profile not in available:
        raise ValueError('Unknown profile: ' + profile)

    rules = available[profile]['rules'] if profile else sorted({
        name for cfg in available.values() for name in cfg['rules']
    })
    skills = available[profile]['skills'] if profile else skill_names()
    parts = [
        '# AI Engineering guidance',
        f'Project: {root}\nProfile: {profile or "baseline (no repository profile inferred)"}',
        'User instructions, project-local instructions and the existing public API take '
        'precedence over this shared guidance. Apply conventions only where relevant '
        'and where local policy is silent. Read local CLAUDE.md, AGENTS.md and rules first. '
        'Profiles describe context; verify them against the actual repository.',
    ]
    if profile:
        parts.append(read(f'profiles/{profile}.md').strip())
    parts.extend(read(f'rules/{name}.md').strip() for name in rules)
    parts.append('## Task skills\n\nRead only relevant skills by running:\n\n' + '\n'.join(
        f'- `ai-engineering skill {name}` — {skill_description(name)}' for name in skills
    ))
    return '\n\n'.join(parts) + '\n'
