---
name: parallel-concurrency
description: Review correctness and performance of task queues and parallel backends.
---

# Parallel Concurrency

1. Confirm ownership, thread lifetime, cancellation/shutdown and exception handling.
2. Test races, missed wakeups, task loss, nested scheduling and work-stealing bounds.
3. Compare std::thread/OpenMP/TBB where available and configured.
4. Vary thread count, grain size and workload skew; verify deterministic reductions where promised.
5. Use sanitizers where supported, and report nondeterministic failures.
