# AI-Engineering

Shared Claude Code, Cursor and AGENTS.md instructions for KhwarizmiAnalytix C++ libraries.

This is a **ready-to-publish repository scaffold**, not an already-created GitHub remote. Sources and provenance are documented in `docs/provenance.md`. Shared practices are separated from repo-specific overlays. Project-local guidance and user changes take precedence.

## Contents

- `src/ai_engineering/rules/`: source-of-truth Markdown policies.
- `src/ai_engineering/skills/`: task-oriented `SKILL.md` bundles.
- `src/ai_engineering/profiles/`: per-repository contexts and selected skills.
- `src/ai_engineering/installer.py` / `cli.py`: the installer logic and the `ai-engineering` console command.
- `agents/`: specialist Claude Code agent profiles.
- `scripts/install.py`, `scripts/validate.py`: dev-mode wrappers for working inside this checkout without installing the package.
- `.claude-plugin/marketplace.json`: Claude Code plugin marketplace entries.
- `plugins/`: small Claude plugins based on the shared skill files.
- `.cursor/rules/`: example Cursor rules for *this* repo; installer generates rules for target projects.

## Install as a Python package

```sh
pip install git+https://github.com/KhwarizmiAnalytix/AI-Engineering.git
# or, from a local checkout:
pip install .

ai-engineering list-profiles
ai-engineering install --project ../LinearAlgebra --profile LinearAlgebra --dry-run
ai-engineering install --project ../LinearAlgebra --profile LinearAlgebra
ai-engineering install --project ../Solvers --profile Solvers
```

This packages `src/ai_engineering/{rules,skills,profiles}` as module data, so the `ai-engineering` command works standalone in any environment — no AI-Engineering checkout required on the target machine. Pin a version in the consuming project's own dependency file to control upgrades.

## Install from a checkout (no pip install)

```sh
python scripts/install.py --project ../LinearAlgebra --profile LinearAlgebra --dry-run
python scripts/install.py --project ../LinearAlgebra --profile LinearAlgebra
python scripts/install.py --project ../Solvers --profile Solvers
python scripts/validate.py
```

Both routes run the same installer. The installer creates `.cursor/rules/ai-engineering-*.mdc`, `.claude/rules/ai-engineering-*.md`, `.claude/skills/ai-engineering-*/SKILL.md`, and `AI_ENGINEERING.md`. It **does not replace** your existing `CLAUDE.md`, `AGENTS.md`, `.augment/rules`, or skills. Append an instruction in your existing `CLAUDE.md` and `AGENTS.md` to consult `AI_ENGINEERING.md`, or use the opt-in `--entrypoints` option to append a managed reference block.

Re-run with `--force` to update *only installer-managed files*. Changed managed files are backed up before replacement. Run `--dry-run` first.

## Claude Code plugin route

```text
/plugin marketplace add KhwarizmiAnalytix/AI-Engineering
/plugin install cpp-core@khwarizmi-ai-engineering
/plugin install numerical@khwarizmi-ai-engineering
/plugin install gpu@khwarizmi-ai-engineering
```

The plugin delivery is an **alternative** to local copying. Avoid installing both routes for the same skills without a reason. The marketplace metadata is a candidate configuration and has not been live-tested against a Claude Code installation here.

## Precedence

User instruction > target repo's `CLAUDE.md` or `AGENTS.md` and public API > repo-local existing rules > the AI-Engineering shared rules. Never silently change established public API, build flags, or error conventions.

## Publish

```sh
cd AI-Engineering
git init && git add . && git commit -m "Initial shared agent rules and skills"
gh repo create KhwarizmiAnalytix/AI-Engineering --private --source=. --remote=origin --push
```

The `gh` command requires an authenticated GitHub CLI session with rights to the organization. Choose `--public` instead of `--private` if desired.
