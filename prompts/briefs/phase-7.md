# Phase 7 brief — harden

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 7.

**Required seats:** all six voting seats.

---

## Do

1. All tests in `references/quality.md`.
2. Public `__all__` scanned for banned names.
3. production profile: durable once-store, receipts on; doctor fails
   that profile if either is missing.
4. Async Action: sync submit refuses; `async_submit` runs it.
5. No leftover names in docs or examples.
6. Every `open` pre-mortem corner is `absorbed` or an explicit `wont`
   with a live-file citation.
7. Day-1 acceptance: one file, <40 lines, cart morphs, no Intent /
   CapService / stamp / preview.

## Corners

C-pre-31, C-pre-32, and every execution row in CORNERS.md.

## Exit

This gate Advances. The library is done.
