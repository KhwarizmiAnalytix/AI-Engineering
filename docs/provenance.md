# Provenance and verification

Reviewed public repository pages on 2026-10-25. This package paraphrases/adapts shared guidance; it does **not** claim to be an exact mirrored snapshot. No repository was modified or pushed.

- Solvers: https://github.com/KhwarizmiAnalytix/Solvers/blob/master/CLAUDE.md
- LinearAlgebra: https://github.com/KhwarizmiAnalytix/LinearAlgebra/blob/main/CLAUDE.md
- Memory: https://github.com/KhwarizmiAnalytix/Memory/blob/main/CLAUDE.md
- Parallel: https://github.com/KhwarizmiAnalytix/Parallel/blob/main/CLAUDE.md
- Logging: https://github.com/KhwarizmiAnalytix/Logging/blob/main/CLAUDE.md
- Common coding source: https://github.com/KhwarizmiAnalytix/LinearAlgebra/blob/main/.augment/rules/coding.md
- Builder source: https://github.com/KhwarizmiAnalytix/LinearAlgebra/blob/main/.augment/rules/builder.md
- Common project-build skill: https://github.com/KhwarizmiAnalytix/LinearAlgebra/blob/main/.claude/skills/project-build/SKILL.md

Verified recurring patterns: per-repo CLAUDE instructions, .augment rules and .claude skills; shared Python setup and optional Bazel setup; Testing/Cxx patterns; CMake colon formatting; C++ snake_case and builder conventions; preserve local APIs and dependencies.

New proposed, not verified existing policies: detailed specialized numerical, GPU, benchmark and scalar skills; installer behavior; plugin packaging. Scalars repository rules were not verified, so its profile is provisional.

Known differences: Logging README currently says embedded `add_subdirectory` is supported but complete installed `find_package(Logging CONFIG REQUIRED)` is *not*. Do not claim it works before fixing/testing. LinearAlgebra explicitly prohibits implicit host transfers for device-pointer GPU backends. Solvers includes a mix of native and optional third-party backends.

## Shared Python tool delivery (2026-10-27)

Version 0.2.0 keeps policy and workflow bodies in package resources and adds read-only `context` and `skill` commands. User setup registers thin runtime loaders, without generating project files. Existing policies and repository profiles have not been changed or reverified against upstream repositories for this delivery change.

Integration locations were checked against official documentation:

- Claude user rules: https://code.claude.com/docs/en/memory#user-level-rules
- Claude personal skills: https://code.claude.com/docs/en/skills
- Cursor user skills, including compatibility discovery from `~/.claude/skills/`: https://cursor.com/docs/skills
- Cursor User Rules: https://cursor.com/docs/rules

Cursor automatic baseline loading uses a one-time User Rule pasted into Settings. Setup prints and saves that text rather than depending on undocumented editor settings storage. No real user settings or consuming repositories were modified during implementation. Automated checks exercise temporary homes; live Claude Code and Cursor discovery remains unverified.

The requested public distribution name is `ai-enegennr`; the Python import remains `ai_engineering` and the console command remains `ai-engineering`. The PyPI JSON endpoint returned HTTP 404 for that name on 2026-10-27; this does not reserve the name or guarantee PyPI will accept it. The release workflow follows https://docs.pypi.org/trusted-publishers/using-a-publisher/ and requires the account owner to configure the corresponding publisher on PyPI.

## Bazel third-party ownership rule (2026-10-30)

Added to `rules/dependencies.md`, adapted from `docs/BAZEL_THIRD_PARTY_MIGRATION_PLAN.md` in the
Vectorization repository (local file, not yet published upstream at the time of this change):
each repo should own the Bazel overlay for the third-party dependencies it vendors, and consumers
should depend only on the owning sibling module, never redeclare a third-party repo they don't
vendor just to satisfy a sibling's transitive closure. The caveat about `override_*` directives
being root-module-only, and about repo-authored `ThirdParty/*.BUILD` overlays counting as "the
repo's own code" for the direct-reference check, came from applying the plan against the live
`MODULE.bazel` files in LinearAlgebra, Logging, Memory, Numericals, Parallel, Profiler, random,
Serialization, Solvers, Vectorization and Graph, not from the plan document itself.
