---
name: project-build
description: Configure, build and test the target C++ project using its documented scripts and toolchains.
---

# Project Build

1. Inspect `CLAUDE.md`, README, CI and `Scripts/setup.py --help` if present.
2. Identify applicable CMake/Bazel presets, compilers and optional dependencies.
3. Configure/build affected targets and run focused tests; broaden if needed.
4. Test installation and external consumer `find_package` when package interfaces change.
5. Report exact commands, test status, environment and blockers.
