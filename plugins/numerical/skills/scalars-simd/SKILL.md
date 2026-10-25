---
name: scalars-simd
description: Implement and validate floating, complex and SIMD scalar operations.
---

# Scalars Simd

1. Define scalar representation, ABI and accuracy requirements before coding.
2. Verify IEEE-754 edge cases for half/bfloat16, complex, NaN, signed zero and infinities.
3. Keep scalar and SIMD paths numerically consistent within specified error bounds.
4. For complex transcendentals preserve branch cuts and safe scaling; SVML only supplies real vector primitives.
5. Verify feature gating and fallback on non-AVX platforms.
