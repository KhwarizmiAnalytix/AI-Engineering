---
name: numerical-validation
description: Validate numerical algorithms against references, theory and difficult inputs.
---

# Numerical Validation

1. Identify mathematical assumptions, complexity, conditioning and stability concerns.
2. Select literature or trusted BLAS/LAPACK/MKL/PyTorch/Eigen references; inspect actual algorithms rather than README claims.
3. Test float/double and complex when supported: zero, tiny, huge, singular, rank deficient and ill-conditioned cases.
4. Use backward/forward errors, residuals, orthogonality and relative error scaled to conditioning.
5. Check NaN, infinity, signed zero, branch cuts and exception/error contracts; report differences precisely.
