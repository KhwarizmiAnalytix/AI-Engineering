---
name: clang-tidy
description: Run targeted C++ static analysis and distinguish introduced findings from baseline noise.
---

# Clang Tidy

1. Locate the project `.clang-tidy` and compilation database.
2. Restrict checks to touched first-party translation units.
3. Compare new findings with baseline; prioritize safety and correctness.
4. Do not blindly apply semantic-changing fixes.
5. Report the exact command and remaining findings.
