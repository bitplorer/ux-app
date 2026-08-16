# Phase 2 brief — Component + State

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 2.

**Required seats:** Document, Author, Channel, Adversary.

---

## Do

1. A class with `id` + `render` is a Component. Honor ux-dom
   `Component` / `ReactiveComponent` if subclassed — do not wrap twice.
2. Dataclass fields default to session. Markers: `Client()`, `Store()`,
   `Transient()`, `Sealed()`.
3. Client keys must be on the allowlist. Money-shaped names on client
   fail the type gate and doctor.
4. `on_click=` / `on_submit=` mint Caps in the adapter with the args
   the handler will see (including defaults).
5. Integer sealed fields: no silent coerce.

## Corners

C-pre-08 … C-pre-11.

## Exit

Render a badge Component; click path exists; Cap is present on the
control (`data-action`, `data-cap`, `data-args`).
