# Builds and package integration

- Inspect README, CI, `Scripts/setup.py --help`, `CMakeLists.txt`, toolchain and presets before guessing commands or flags.
- For repositories with `Scripts/setup.py`, prefer its documented `config.build.test` action; use `Scripts/setup_bazel.py config.build.test` where Bazel exists.
- Verify CMake and Bazel impacts separately; do not assume identical file discovery.
- Validate install/export targets, transitive dependencies, namespace aliases, and `find_package` from an external consumer.
- Maintain the local CMake configuration-summary colon alignment rule where present (colon at character 24 including opening quote).
- Avoid changing third-party directories unless explicitly requested.
