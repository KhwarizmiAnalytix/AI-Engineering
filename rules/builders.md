# Builder conventions

Apply only to code that already needs builders.
- Name a new builder type with `_builder` suffix.
- Use one-argument fluent `with_<field>` setters when compatible with the existing API.
- Preserve namespace, ownership and exported-interface conventions of the owning repository.
- Document construction constraints, state transitions, and transfer of ownership.
