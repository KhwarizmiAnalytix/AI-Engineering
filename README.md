# AI-Engineering

Install shared engineering rules and skills as a Python tool, then register it once for Claude Code and Cursor across your local projects. Full guidance stays inside the installed package. Projects need no generated `CLAUDE.md`, `.claude/`, `.cursor/`, or skill copies for this workflow.

The PyPI distribution is named `ai-enegennr`; its command is `ai-engineering`. Python 3.9 or newer is required. The package has no runtime dependencies.

## Install once

Once the first release has been published to PyPI:

```sh
pip install ai-enegennr
ai-engineering setup --user --dry-run
ai-engineering setup --user
```

For an isolated command available across projects, use `pipx install ai-enegennr` instead of `pip install ai-enegennr`. Keep the command available on the PATH used by your editor and agent. Installing into a project-only virtual environment makes the command available only while that environment is active.

For development before a PyPI release, install from the checkout with `python3 -m pip install .`, or from Git after these changes are pushed:

```sh
python3 -m pip install git+https://github.com/KhwarizmiAnalytix/AI-Engineering.git
```

A built wheel can also be installed directly with `python3 -m pip install dist/ai_enegennr-0.2.0-py3-none-any.whl`.

## Connect your agents

`ai-engineering setup --user` creates small user-level registrations:

- `~/.claude/rules/ai-engineering.md` asks Claude Code to load shared context at the start of repository work.
- `~/.claude/skills/ai-engineering*/SKILL.md` registers task workflows for Claude Code and Cursor. Cursor supports this compatibility location, so the default setup needs only one set of entries.
- `~/.config/ai-engineering/cursor-user-rule.md` contains the one-time Cursor User Rule. Setup also prints its text. Paste it into **Customize → Rules → User Rules** to request shared context automatically in every project.
- `~/.config/ai-engineering/managed.json` tracks these registrations for safe updates and removal.

Start a new agent session after setup. Skills are available as `/ai-engineering` and `/ai-engineering-project-build`, for example. Each registration tells the agent to read the current workflow through the installed command; full rule and skill contents are not copied into these entries.

Use `--tool claude` for Claude-only setup or `--tool cursor` for Cursor-only setup. Cursor-only setup registers skills under `~/.cursor/skills/`. Use the same tool selection for subsequent setup runs; uninstall first when switching layouts.

The discovery locations follow the official [Claude rules](https://code.claude.com/docs/en/memory#user-level-rules), [Claude skills](https://code.claude.com/docs/en/skills), [Cursor skills](https://cursor.com/docs/skills), and [Cursor User Rules](https://cursor.com/docs/rules) documentation. Local registrations apply on the machine where they are installed. Remote workers need the package and registrations in their own environment. Agent instructions request behavior; they are not enforcement hooks. Live editor discovery has not been tested here.

## Use in any project

```sh
ai-engineering context --project ../Logging
ai-engineering context --project ../renamed-checkout --profile LinearAlgebra
ai-engineering skill project-build
ai-engineering list-profiles
ai-engineering list-skills
python3 -m ai_engineering --help
```

`context` and `skill` print guidance without writing files. Context finds the repository root from a nested directory using `.git`, `pyproject.toml`, or a known profile directory name. It selects a profile by root directory name, ignoring case. Unrecognized repositories receive baseline conventions and the skill catalog without a guessed project profile. Use `--profile` for renamed checkouts or worktrees.

Profiles describe repository context and select relevant skills; they do not override local instructions. User instructions, project-local guidance, and the actual public API take precedence over shared defaults. Only load skills relevant to the task.

## Update or remove

Upgrade the package, then refresh the small registrations:

```sh
python3 -m pip install --upgrade ai-enegennr
ai-engineering setup --user
```

For pipx installations, use `pipx upgrade ai-enegennr` before setup. Updated rules and workflow bodies are read from the upgraded package immediately; rerunning setup registers added skills and refreshes descriptions. Start a new session to refresh agent discovery and previously loaded context.

Setup preserves unmanaged files and locally modified registrations. Unmodified managed entries update automatically. Use `--force` to replace a modified managed entry after saving a numbered backup. Conflicts produce a nonzero exit status. `--dry-run` writes nothing. `--home /some/home` supports a custom home or a disposable preview directory.

```sh
ai-engineering uninstall --user --dry-run
ai-engineering uninstall --user
python3 -m pip uninstall ai-enegennr
```

Uninstall removes only unchanged managed registrations, preserves local edits and backups, and leaves native instruction files alone. Remove the pasted Cursor User Rule through Settings yourself. Run integration uninstall before removing the Python package.

## Existing project-copy workflow

The previous installer remains available for environments that require repository-local delivery:

```sh
ai-engineering install --project ../LinearAlgebra --profile LinearAlgebra --dry-run
ai-engineering install --project ../LinearAlgebra --profile LinearAlgebra
```

This explicitly copies guidance into a single project. It is separate from the recommended shared-package workflow. `--entrypoints` appends a managed reference to `CLAUDE.md` and `AGENTS.md`; `--force` updates managed copies and backs up local modifications. Checkout wrappers under `scripts/` remain compatible.

User-level setup does not remove copies created by the older installer. When migrating, review the target project's `.ai-engineering-managed.json` and remove only obsolete generated entries after checking for local edits. Preserve the project's own instructions.

The `plugins/` and `.claude-plugin/marketplace.json` assets provide an alternative Claude plugin route. Their candidate configuration has not been live-tested. Avoid registering the same workflows through multiple delivery routes.

## Development

```sh
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 -m pip install build
python3 -m build
```

Source policies live in `src/ai_engineering/rules/`, workflows in `src/ai_engineering/skills/`, and repository contexts in `src/ai_engineering/profiles/`. Tests use temporary homes and do not alter real agent settings. CI checks Python 3.9, 3.12, and 3.14, including installed commands outside the checkout.

Sources, contextual limitations, and verification are recorded in [docs/provenance.md](docs/provenance.md).

## Publish to PyPI

The `publish.yml` workflow builds and checks both distributions, tests the installed wheel, and publishes through PyPI Trusted Publishing. It runs when a GitHub release is published or when dispatched manually. Release tags must match the package version, such as `v0.2.0`.

Before the first publication, a PyPI account owner must register a [pending Trusted Publisher](https://pypi.org/manage/account/publishing/) with these exact values:

| Field | Value |
| --- | --- |
| PyPI project name | `ai-enegennr` |
| GitHub owner | `KhwarizmiAnalytix` |
| Repository | `AI-Engineering` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

After registration, push the workflow to GitHub and publish the matching release, or run `gh workflow run publish.yml --repo KhwarizmiAnalytix/AI-Engineering`. No API token is needed with Trusted Publishing. See the [official setup guide](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

After a successful upload, verify public installation in a fresh environment with `python3 -m pip install --index-url https://pypi.org/simple ai-enegennr` and `ai-engineering --version`.
