# Phase 1 brief — adapter + boot

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 1.
Procedure: [COUNCIL.md](../COUNCIL.md).

**Required seats at the gate:** Channel, Document, Domain, Adversary.

---

## Do

1. `App.boot(title=..., cek="off")` creates Document + Channel when
   cores are installed; otherwise LocalRuntime (in-process Host+Peer).
2. Default domains `{baseline, ui}` → session pair set = S.
3. Default Layout, one content region (`content`) plus `notices`.
4. Inject scripts: Peer kernel **then** preview.
5. `App.bind(document=..., channel=...)` for tests.
6. Isolation doctor runs at boot when `strict=True`.
7. Cold `import ux_app` does not import Channel / CEK / codecs.
8. `cek=off` still refuses undeclared pairs (C-pre-06).

## Do not

- Import `ux_channel` / `cek_*` outside `adapter/`.
- Attach preview before the Peer kernel.
- Invent a second Channel.

## Corners

C-pre-03 … C-pre-07, C-pre-34.

## Exit

A test boots App, renders an empty page with scripts present (kernel
before preview), doctor green, pair set = S.
