---
name: memory-allocator
description: Review CPU and GPU allocation and caching behavior.
---

# Memory Allocator

1. Characterize allocator ownership and `data_ptr`/`retained_ptr`/`data_view` lifetimes.
2. Check alignment, zero-byte allocation, frees, device/stream correctness and exception safety.
3. Cover caching allocator fragmentation, reuse, pool pressure, concurrency and GPU synchronization.
4. Measure cold allocation, warm reuse and mixed-size patterns separately.
5. Compare with matched external allocators without changing benchmark semantics.
