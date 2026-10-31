# Dependencies and scope

- Inspect `ThirdParty/`, lock files, Bazel modules and CMake options before adding a dependency.
- Do not replace an existing backend or vendor source without demonstrating the need.
- Keep optional backends optional and compile cleanly when absent.
- Avoid broad refactors, unrelated renames, and unsolicited tracking documents.

## Bazel third-party ownership

Each repo owns the Bazel overlay for the *external* third-party
dependencies it vendors under its own `ThirdParty/` (e.g. `fmt`,
`magic_enum`, `mimalloc`, `loguru`, `glog`, `gflags`, `eigen`). Consumers
depend only on the owning sibling module (`@logging`, `@memory`, ...),
never directly on an external third-party repo they don't vendor
themselves — mirrors PyTorch's per-module `third_party/<dep>.BUILD`
ownership (`WORKSPACE`).

This applies only to external third-party libraries, not to sibling
KhwarizmiAnalytix module dependencies (`xsigma_logging`, `xsigma_memory`,
`xsigma_linearalgebra`, `xsigma_scalars`, `xsigma_profiler`, ...). A sibling
module wired into `MODULE.bazel` but not yet referenced by any target is
kept, not removed — it may be there for near-term/future use, and the
project owner decides when it's genuinely dead, not a grep hit.

- Before adding an *external* third-party repository declaration to
  `MODULE.bazel`, check whether the repo's own code — including any
  `ThirdParty/*.BUILD` overlay the repo itself authored to rebuild a
  vendored sibling's sources — references it directly. If nothing in the
  repo does, the declaration belongs to whichever repo vendors that
  dependency; don't declare it here just to satisfy a sibling's transitive
  closure.
- A declaration that looks unreferenced by grep may still be load-bearing:
  Bazel's module `override_*` directives (`local_path_override`, etc.) only
  take effect from the root module, so a sibling dependency's own override
  is silently dropped once that sibling is non-root. Verify empirically —
  remove the declaration, then build and test the repo both standalone and
  as a downstream dependency — rather than deleting on grep evidence alone.
