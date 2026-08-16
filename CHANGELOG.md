# Changelog

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
