---
name: cmake-package
description: Audit CMake packaging, exports and installed consumer compatibility.
---

# Cmake Package

1. Inspect target names, install/export statements and config/version package generation.
2. Build and install into a clean prefix.
3. Compile an external `find_package(... CONFIG REQUIRED)` consumer and inspect transitive dependencies.
4. Validate multi-config and static/shared cases where supported.
5. Distinguish supported embedded builds from unsupported installed-package builds.
