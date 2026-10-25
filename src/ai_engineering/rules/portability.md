# Portability

- Target the language level and platforms required by each repository; do not silently require a newer compiler.
- Guard SIMD, CUDA, HIP, Metal, MKL and platform-specific code with the project's feature checks.
- Keep CPU-only builds operational if the project supports them.
- Never silently move device arrays to host memory; make transfers and sync explicit.
