# Phase 5 brief — events + preview

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 5.

**Required seats:** Law, Domain, Author, Adversary.

---

## Do

1. `ctx.follow_up(event, action, args_from=...)` mints a continuation
   Cap on the Host.
2. Peer fills declared slots only. Host verifies the sealed args again,
   then dispatches with filled slots (`_trusted` after that verify).
3. Bound inputs automatically coalesce / pending (Peer preview).
4. `preview.pending` / `preview.update` / `preview.filter` exist as
   escape hatches and are illegal inside returned Ops.
5. Next Result clears preview, then applies Ops.
6. Preview must not write authority kv. Peer has no `mint`.

## Corners

C-pre-24 … C-pre-28, C-pre-33 (do not re-export leftover verbs).

## Exit

Debounce-style search type → follow-up commit; preview gone after
Result; Peer cannot fire the follow-up without the Host Cap.
