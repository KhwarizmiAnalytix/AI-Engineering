---
name: benchmarking
description: Run defensible reproducible performance comparisons without misleading claims.
---

# Benchmarking

1. Fix build type, compiler flags, thread counts, backend, device and allocator settings.
2. Separate warm-up/cold path and setup/allocation from steady-state kernel timing.
3. Match precision, dimensions, memory location and work across baselines.
4. Capture variance, repeats and correctness; GPU timings require explicit synchronization or device events.
5. Report throughput, latency, scaling and known limitations; avoid cross-machine absolute comparisons.
