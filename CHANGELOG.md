# Changelog

## 0.2.0 — 2026-08-16

S-tier component battery + in-framework radical enhancements. Isolation,
Cap law, pair identity, and `notify()` S-only expansion are unchanged.

- ux-dom UI kit extended: Slider, Carousel, ToastHost, DatePicker, Chart,
  TableEmpty / TableCaption, Dialog a11y, Switch thumb, progressive
  `public_form`. Ownership stays in `ux_dom.ui`.
- Author DX: `from ux_app.ui import …` re-exports the kit when ux-dom is
  installed. `uxapp add ui <Name>` copies via `uxdom add ui`.
- Bundled `effects` DomainPack: `ui.notice.push` / `ui.notice.clear` +
  `effects_driver`. `notify()` still expands only to S pairs.
- Doctor UI health: `app.require_composite` / `app.declare_runtime`.
  Production profile fails undeclared Alpine for Tabs/Dialog/Carousel.
- Golden paths: checkout follow_up Cap, preview-then-commit search,
  transactional multi-region `list[Op]`, morph × Alpine coexistence markup.
- Docs: `COMPONENTS.md`.

## 0.1.0 — 2026-08-16

Initial public release.

- Author API: `App`, `Component`, `action`, `update` / `notify` / `go`,
  `follow_up`, `preview`, field planes (`Client`, `Store`, `Transient`,
  `Sealed`), `Badge`
- Isolation: only `adapter/` may import `ux_channel` / `cek_*`
- `LocalRuntime` in-process Host + Peer so `App.bind()` and tests run
  without unpublished cores
- Caps: HMAC tokens (`base64url(json).sig`), once-store, sealed args
- Domains: stamp + driver path; bundled `search` pack
- CLI: `uxapp create-app | init | new | doctor | explain`
- Golden cart: `examples/cart.py` morphs badge `0 → 1`
- `make verify` — pytest, isolation scan, public `__all__`, doctor
