# Testing and verification

- Read adjacent `Testing/Cxx/Test*.cpp` or `Test*.cxx` before adding cases. Match its test framework, discovery and naming.
- Test normal, boundary, invalid, degenerate, numerically difficult and concurrency cases as relevant.
- Use deterministic seeds and tolerances informed by conditioning, magnitude and floating-point type; never use a single arbitrary global tolerance.
- Verify CPU/GPU backends against a trusted reference and test backend-specific behavior.
- Review the diff and run relevant lint/static analysis after substantive changes. Report actual commands/results and unavailable tools.
- Respect Bazel package globs and required registration of new test directories.
