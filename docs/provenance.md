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
