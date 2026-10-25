# Dependencies and scope

- Inspect `ThirdParty/`, lock files, Bazel modules and CMake options before adding a dependency.
- Do not replace an existing backend or vendor source without demonstrating the need.
- Keep optional backends optional and compile cleanly when absent.
- Avoid broad refactors, unrelated renames, and unsolicited tracking documents.
