---
name: gpu-kernels
description: Design and review CUDA/HIP GPU kernels and host-device integration.
---

# Gpu Kernels

1. Check backend feature macros and pointer ownership before touching kernels.
2. Ensure there are no unintended host-device transfers or synchronizations.
3. Validate strides, layouts, aliasing, streams, launch errors and asynchronous lifetimes.
4. Compare results to CPU reference for multiple sizes/dtypes and stress errors.
5. Benchmark warm and cold paths with correct GPU timing.
