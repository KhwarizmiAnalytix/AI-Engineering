# AI-Engineering

Shared Claude Code, Cursor and AGENTS.md instructions for KhwarizmiAnalytix C++ libraries.

This is a **ready-to-publish repository scaffold**, not an already-created GitHub remote. Sources and provenance are documented in `docs/provenance.md`. Shared practices are separated from repo-specific overlays. Project-local guidance and user changes take precedence.

## Contents

- `rules/`: source-of-truth Markdown policies.
- `skills/`: task-oriented `SKILL.md` bundles.
- `agents/`: specialist Claude Code agent profiles.
- `profiles/`: per-repository contexts and selected skills.
- `scripts/install.py`: safe copying into a target repository, with dry-run, non-overwrite by default, and managed-file manifest.
- `.claude-plugin/marketplace.json`: Claude Code plugin marketplace entries.
- `plugins/`: small Claude plugins based on the shared skill files.
- `.cursor/rules/`: example Cursor rules for *this* repo; installer generates rules for target projects.

## Install into a project

```sh
python scripts/install.py --project ../LinearAlgebra --profile LinearAlgebra --dry-run
python scripts/install.py --project ../LinearAlgebra --profile LinearAlgebra
python scripts/install.py --project ../Solvers --profile Solvers
python scripts/validate.py
```

The installer creates `.cursor/rules/ai-engineering-*.mdc`, `.claude/rules/ai-engineering-*.md`, `.claude/skills/ai-engineering-*/SKILL.md`, and `AI_ENGINEERING.md`. It **does not replace** your existing `CLAUDE.md`, `AGENTS.md`, `.augment/rules`, or skills. Append an instruction in your existing `CLAUDE.md` and `AGENTS.md` to consult `AI_ENGINEERING.md`, or use the opt-in `--entrypoints` option to append a managed reference block.

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
