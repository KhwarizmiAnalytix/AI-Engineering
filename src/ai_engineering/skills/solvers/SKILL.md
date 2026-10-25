---
name: solvers
description: Review nonlinear solvers, calibration, derivatives and convergence behavior.
---

# Solvers

1. Classify problem: roots, least squares, scalar optimization, constraints and derivatives.
2. Match native and optional backends to actual capabilities (Ceres, Ipopt, NLopt, PETSc/TAO as available).
3. Verify trust-region/line-search acceptance, Jacobian accuracy, scaling and stopping conditions.
4. Benchmark on named literature problems, stiff/ill-conditioned cases and regression cases.
5. Never label an alternative update globally convergent without proof; report failure modes.
