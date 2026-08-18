# Council Decision — Stack cleanup (crossings, naming, no fifth kernel)

**Date:** 2026-08-18
**Question:** How do we isolate repeated Host crossings so the stack stays
clean, named correctly, and antifragile at FAANG scale — without a fifth
core or a taken name?
**Strategy:** halt-or-patch · primary sources · adversary stress
**Outcome:** Binding placements + this release’s implementation scope

---

## 1. Seats

| Seat | Mandate |
|------|---------|
| **Law** | Two kernels only. Isolation. One intent → one name. |
| **Channel** | Wire, Caps, `applyMorph`. Does not learn `transition.*`. |
| **Document** | Markup, `document.use`, tokens. No Op fold. |
| **Motion** | Plan IR, HOFs, player. Soft peer of Channel. |
| **Author** | `update` / `notify` / `go` / ports. Adapter is the door. |
| **Adversary** | Fifth package, dual Button, `reply()`, `glue.js`, ux-surface revival. |
| **Host** | `#view`, pantry, `img-{sku}`, toast TTL, brand. |

---

## 2. North star (unanimous)

> Each kind of truth lives in exactly one place.
> Cores never hard-import each other.
> A crossing is glue named after both peers, an adapter wall, a Document
> contribution, or an optional door — never a Host file called “glue”.

`ux-app → ux-channel → cek-surface` is **not** a hard MRO.
CEK is reached through `ChannelConfig.cek` / `adapter/cek.py` only.
`cek_surface` must not import `ux_channel` (D4).

---

## 3. Rejected (kill criteria)

| Move | Why it dies |
|------|-------------|
| New `ux-kit` / `ux-paint` / `ux-glue` package | Third owner; version skew |
| Revive `ux-surface` / `uxkit` | Predecessor; `surface.ui` is a second design system |
| Name the compositor `glue.js` | **Glue** is already `ux_channel_ux_dom` |
| Call it a Bridge | Bridge = npm islands |
| Put JS hooks in `ux_app.adapter` | Adapter is the Python import wall |
| Teach Channel `transition.*` | Pollutes the immortal op table |
| New `ux_channel_ux_motion` *repo* | A contribution is enough; don’t mint a package for 40 lines of JS |
| `reply(*effects)` on `ux_app` | Banned public name; dual finish API vs `list[Op]` |
| Full Harbor isolation of VEIN in this pass | Product rewrite (`@ch.on` → `App.boot`); not a library crossing |
| Promote `#view` / pantry / toast TTL | One Host; promote only when three independent Hosts need it |

---

## 4. Binding placements

| Crossing | Home | Name |
|----------|------|------|
| Op+tree → Channel idiomorph | `ux_app.adapter.lower_morph` | **lower** |
| Fold Ops + Scenes; XOR law; nav last | `ux_app.adapter.compose` | **compose** |
| `transition.*` after authority morph | `ux_motion.MotionChannel` + `ux-motion-channel.js` | **MotionChannel** |
| Official channel↔dom Python interop | `ux_channel_ux_dom` | **Glue** (taken) |
| Toast TTL, img `src` pin | Host `vein-chrome.js` | Host chrome |
| `#view`, `#img-pantry`, `img-{sku}` | Host | Host |
| Markup / tokens / Button | ux-dom | Document |
| Cap mint / Peer apply | Channel / cek-host via door | Door |

XOR law (compose, fail closed):

```text
on one Result:  morph(T, tree)  XOR  scene.enter(T, html=tree)
```

Motion without `html` on `T` may share the target (animate a just-morphed node).

---

## 5. Why these names (naming constitution)

From Channel NAMING.md: one intent → one preferred name. No third synonym.

| Speech | Write |
|--------|--------|
| “play motion after Channel morph” | `MotionChannel()` · `name="ux_motion.channel"` |
| “author morph to idiomorph wire” | `lower_morph` |
| “fold this Result” | `compose` |
| “channel↔dom Python helpers” | `ux_channel_ux_dom` (Glue) |
| “npm island” | Bridge |
| “import wall” | `ux_app.adapter` |

`MotionChannel` is a **contribution**, same family as `Motion()` / `XElement()` /
`Channel.optional()`. Owner is in the `name`.

---

## 6. Antifragile properties

- Add a new motion HOF → Hosts do not touch Channel.
- Add a Channel op → MotionChannel still peels only `transition.*`.
- Drop Motion → `document.use` without `MotionChannel()`; Channel still morphs.
- Drop Channel → Motion still plays via `UxMotion.applyOps` (no hook needed).
- Lower/compose fail closed (empty target, unknown item, XOR clash).
- Cold `import ux_app` still loads no Channel / CEK.
- Promote path unchanged: markup → ux-dom; ports/adapters → ux-app; never a third core.

---

## 7. This release (implemented)

| Library | Change |
|---------|--------|
| ux-app **0.3.0** | `adapter.lower_morph`, `adapter.compose` + tests |
| ux-motion **1.3.0** | `MotionChannel`, `ux-motion-channel.js`; player `morph` uses `injectHtml` |
| VEIN Host | `paint.py` calls adapter; `document.use(MotionChannel(), Channel.optional())`; `glue.js` removed; `vein-chrome.js` is Host-only |

Deferred (solid, not this pass):

1. VEIN product modules stop importing `ux_channel` (`App.boot` path).
2. Channel `applyMorph` option for identified `<img src>` (needs 3+ Hosts).
3. Thin `refresh(id)` if App owns `id → render()` (Harbor almost does).
4. Dual Badge (`ux_app.html` vs `ux_dom.ui`) — already on OWNERSHIP_COUNCIL.

---

## 8. Verdict

**Approved under halt-or-patch.**

The stack was already in the right *order*. The mess was crossings sitting
in the shop under a taken name. They now live in the adapter and in a
named contribution. No fifth kernel. No revived predecessor.

**End of council record.**
