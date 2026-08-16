# Phase 3 brief — Actions → list[Op]

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 3.

**Required seats:** Law, Channel, Domain, Adversary.

---

## Do

1. `@action("orders.create", caps=[...])`. `caps=()` is the explicit
   public opt-out. Missing `caps=` is a TypeError.
2. Return `list[Op]`. Component method `None` + dirty → `update(self.id)`.
3. Macros: `update` → `ui.dom.morph`; `notify` / `go` lower to S only.
   Never emit undeclared `ui.toast` / `nav.push`.
4. `Op(ns, name, payload)` structure-checks at construction. Stamp is
   enforced at emit (submit). Unknown pair → fail closed, never `ok`
   with a silent empty batch.
5. Verify before compose. Refuse → `ops: []`. Present Cap verifies.
   once-store down → refuse.

## Corners

C-pre-12 … C-pre-17 (C-pre-13 especially).

## Exit

Golden cart — click increments, morph 0→1, refuse-without-cap leaves
the world unchanged.
