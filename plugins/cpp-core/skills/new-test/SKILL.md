---
name: new-test
description: Design and implement regression tests aligned with the project test conventions.
---

# New Test

1. Read target implementations and closest `Testing/Cxx/Test*.cpp` / `.cxx` cases.
2. Reproduce the bug or mathematical contract with deterministic inputs.
3. Test boundaries, degeneracies, invalid values and different scalar precisions.
4. Register new folders with both CMake and Bazel if applicable.
5. Run tests and document tolerances and coverage limitations.
