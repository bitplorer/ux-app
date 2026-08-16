# Mistakes — take ideas, not APIs

The new library is inspired by the bitplorer stack. It is **not** a fork
of `ux-surface`, `uxkit`, or `cek-surface`.

---

## ux-surface — keep the ideas, drop the design

| Idea worth keeping | Mistake to leave behind |
|--------------------|-------------------------|
| Isolation: only the adapter imports Channel | Source-scan as the *only* design; still stubbed `_to_channel_result` |
| Caps on named operations | Closed `Effect` / `KNOWN_KINDS` catalog that cannot grow with domains |
| Public ids for live targets | Invented type `Partial` instead of Component |
| Fail-closed registry | `@shell` / `Frame` / `Main` as a second layout language |
| | `reply(*effects)` as a second IR next to Ops |
| | In-memory `state` never backed by Host planes |
| | `Theme` as a string name |
| | Public words leftover from noisy design talks |
| | Competing `create-app` vs `uxdom create-app` |
| | Acme example commented out — unproven loop |

Do not start from `src/surface/**` and “finish the stub.” Design the
author API first, then an adapter that speaks **live** Channel + optional CEK.

---

## uxkit — keep the ideas, drop the design

| Idea worth keeping | Mistake to leave behind |
|--------------------|-------------------------|
| Drop-in / copied UI primitives | Vendoring `ux_dom` and `ux_channel` **inside** the package |
| Dataclass / descriptor State | SwiftUI cargo-cult (`VStack` as the product story) |
| Security defaults (CSP, CSRF) | Duplicate Channel / Store implementations |
| | `ActionResult(ok, flash, redirect)` parallel to Ops |
| | “Enterprise” checklist without Caps, isolation, or a real wire |
| | Tiny tree that claims a full stack |

Do not vendor cores. Depend on them. Do not reimplement signals or stores.

---

## cek-surface — keep the model, drop the leftover names

cek-surface is the **compose / Peer-IR / carrier** package. This library
is L7 on Channel. Do not become a second cek-surface.

| Idea worth keeping | Mistake to leave behind |
|--------------------|-------------------------|
| Domain stdlibs, agreement, stamp | Shipping `chrome_*` as a public verb |
| `Op(ns, name, payload)` + pair identity | `arm` as the continuation verb |
| Continuations (Host-minted Caps) | `plan()` as if it were a wire IR |
| Two clocks (authority vs perception) | `signal_set` / `navigate_to` presented as domains |
| Python composition, data-only Ops | Carrier kinds as the product story (Channel already transports) |
| | A second `CapService` / `Surface` type next to Channel |

When Channel `cek=require`, continuations come from Channel’s CEK
adapter. This library calls `follow_up`. It does not re-export `arm`.

---

## Anti-patterns (instant reject)

- App-level `import ux_channel` or `import cek_surface`
- Emitting `("nav", "push")` or `("ui", "toast")` without a stamped domain **and** a driver
- Peer mint, or preview writing authority kv
- Silent string→int coerce on sealed qty
- Morph / notify text not HTML-escaped
- A second scaffold that fights `uxdom`
- React / TS in the author API
- Re-exporting `reply`, `Partial`, `shell`, `chrome`, `arm`, `Surface`, `Effect`, `ActionResult`
- Starting from ux-surface or uxkit source and renaming types
- Treating profile as Cap power
- Projecting a stamped extension onto a Peer with no driver and calling it success
