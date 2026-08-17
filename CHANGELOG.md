# Changelog

## Unreleased

### Component Session/Client planes + callable control

- Session/Client/Store field planes bind to Channel state after `App.attach`.
- `App.state` is the adapter/test escape hatch (None offline).
- `App.control` accepts a bound Component method or `@action` function;
  strings remain an escape hatch (`host.control(cart.add, id=sku)`).
- Isolation unchanged: only `adapter/channel.py` imports `ux_channel`.

### Channel-native design system

- Author macros: `open_overlay`, `close_overlay`, `select_region`, `confirm`,
  `form_result` — exported from `ux_app` and `ux_app.overlay`.
- Ports/adapters isolate the session key scheme (`ui.overlay.*`, `ui.select.*`).
  Keys are not on the public package API.
- Doctor: Channel-first Dialog/Tabs/Carousel/Sheet need no Alpine runtime.
  Production fails **alpine-for-open** when a Host still claims Alpine as the
  open/selected path.
- `ux_app.ui` re-exports new ux-dom stems (Sheet, Command, field_classes, …).
- Tests: `tests/test_overlay_ports.py`.

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
