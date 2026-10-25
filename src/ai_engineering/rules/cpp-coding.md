# C++ coding standards

- Use `snake_case` for new functions, classes, namespaces, and enum values; use `snake_case_` for members, not `m_`. Prefer `kConstantName` for new constants unless the neighboring API differs.
- Preserve existing API names; match surrounding code and the target's `.clang-format`, `.clang-tidy`, and language standard.
- New public headers should follow target project conventions (normally `.h` where established), and implementations may be `.cpp` or `.cu` as appropriate.
- Prefer return values/result types for expected failures; preserve published exception contracts and repo-specific logging integration.
- Include standard, external, and project headers in the repository's configured ordering; match local export macros.
- Use RAII and explicit ownership. Bare pointers are non-owning unless a low-level contract says otherwise.
- Validate sizes, ranges, status values, aliasing and thread-safety assumptions. Prefer condition variables over spinning unless measured and justified.
- Never change a proven public interface just to conform to these defaults.
