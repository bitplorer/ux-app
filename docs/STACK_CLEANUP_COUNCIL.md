# Council Decision — Stack cleanup (crossings, naming, no fifth kernel)

**Date:** 2026-08-18
**Status:** Binding. Supersede only with a new council entry that cites a
reopen condition below.
**Question:** How do we isolate repeated Host crossings so the stack stays
clean, named correctly, and antifragile at FAANG scale — without a fifth
core or a taken name?
**Strategy:** halt-or-patch · primary sources · adversary stress
**Outcome:** Binding placements + this release’s implementation scope
**Sister record:** [bitplorer/ux-motion `docs/14-CHANNEL-COMPOSITOR.md`](https://github.com/bitplorer/ux-motion/blob/main/docs/14-CHANNEL-COMPOSITOR.md)
**ADR:** D2.4 in [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)

Read **§9 before you change a crossing.** That section is the
change-assessment checklist this record exists to serve.

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

Two planes:

```text
CEK   cek-framework → cek-runtime → cek-host → cek-surface
 UX   ux-dom  ⟂  ux-channel  ⟂  ux-motion     (peers)
      ux-app  (L7 author; adapter is the only import wall)
      Host    (harbor / VEIN / any product)
```

---

## 3. Rejected (kill criteria)

| Move | Why it dies | What would have broken |
|------|-------------|------------------------|
| New `ux-kit` / `ux-paint` / `ux-glue` package | Third owner; version skew | Netflix pins 0.3, Vercel pins 0.4; two morph compilers |
| Revive `ux-surface` / `uxkit` | Predecessor; `surface.ui` is a second design system | Dual Button, dual tokens |
| Name the compositor `glue.js` | **Glue** is already `ux_channel_ux_dom` | One intent, two names; NAMING.md violated |
| Call it a Bridge | Bridge = npm islands | Word means two things in one stack |
| Put JS hooks in `ux_app.adapter` | Adapter is the Python import wall | Mixing planes; cold-import story dies |
| Teach Channel `transition.*` | Pollutes the immortal op table | Motion cannot be dropped; Channel owns presence |
| New `ux_channel_ux_motion` *repo* | A contribution is enough; don’t mint a package for 40 lines of JS | Package explosion for a hook |
| `reply(*effects)` on `ux_app` | Banned public name; dual finish API vs `list[Op]` | Authors finish two ways |
| Full Harbor isolation of VEIN in this pass | Product rewrite (`@ch.on` → `App.boot`); not a library crossing | Scope bleed; ship the door, not the shop |
| Promote `#view` / pantry / toast TTL | One Host; promote only when three independent Hosts need it | Library absorbs one product’s chrome |

---

## 4. Binding placements

| Crossing | Home | Name | Why here |
|----------|------|------|----------|
| Op+tree → Channel idiomorph | `ux_app.adapter.lower_morph` | **lower** | Speaks Channel *wire shape*; every Host was copying the dict |
| Fold Ops + Scenes; XOR law; nav last | `ux_app.adapter.compose` | **compose** | One Result, one fold, fail closed |
| `transition.*` after authority morph | `ux_motion.MotionChannel` + `ux-motion-channel.js` | **MotionChannel** | Channel stays ignorant; Motion is droppable |
| Official channel↔dom Python interop | `ux_channel_ux_dom` | **Glue** (taken) | Already named after both peers |
| Toast TTL, img `src` pin | Host `vein-chrome.js` | Host chrome | One Host; 3-host rule |
| `#view`, `#img-pantry`, `img-{sku}` | Host | Host | Visual identity, product layout |
| Markup / tokens / Button | ux-dom | Document | Ownership council |
| Cap mint / Peer apply | Channel / cek-host via door | Door | Isolation law |

XOR law (compose, fail closed):

```text
on one Result:  morph(T, tree)  XOR  scene.enter(T, html=tree)
```

**Why XOR:** both write the same node. Channel idiomorph then motion
`injectHtml` remounts identified images (`img-{sku}`) and flashes decoded
bitmaps. Motion **without** `html` on `T` may share the target (animate a
just-morphed node — `notice("#toast-n")` after `morph("#toasts", …)`).

Navigate / `push_url` / `reload` are ordered **last** so a morph is not
abandoned mid-apply.

Two identity schemes stay separate:

| Scheme | Attribute | Meaning |
|--------|-----------|---------|
| Visual | `id=` / `#view` / `img-{sku}` | Morph identity, bitmap reuse |
| Trust | `data-channel-id` | Caps / Peer. Never merge with `id=` |

---

## 5. Why these names (naming constitution)

From Channel NAMING.md: one intent → one preferred name. No third synonym.

| Speech | Write | Must not write |
|--------|--------|----------------|
| “play motion after Channel morph” | `MotionChannel()` · `name="ux_motion.channel"` | `glue.js`, `Bridge`, `ux_channel_ux_motion` |
| “author morph to idiomorph wire” | `lower_morph` | `to_channel`, `as_op`, `paint` |
| “fold this Result” | `compose` | `reply`, `effects`, `merge_ui` |
| “channel↔dom Python helpers” | `ux_channel_ux_dom` (Glue) | any other “glue” |
| “npm island” | Bridge | — |
| “import wall” | `ux_app.adapter` | — |

`MotionChannel` is a **contribution**, same family as `Motion()` / `XElement()` /
`Channel.optional()`. Owner is in the `name`.

`lower` / `compose` are **not** on `ux_app.__all__`. Author vocabulary stays
`update` / `notify` / `go`. The adapter is the door, not a second author API.

---

## 6. Antifragile properties

These must still hold after any future change. If a patch breaks one, it
is refused.

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
| VEIN Host | `paint.py` calls adapter; `document.use(MotionChannel(), Channel.optional())`; Host-local compositor removed; `vein-chrome.js` is Host-only |

Deferred (solid, not this pass):

1. VEIN product modules stop importing `ux_channel` (`App.boot` path).
2. Channel `applyMorph` option for identified `<img src>` (needs 3+ Hosts).
3. Thin `refresh(id)` if App owns `id → render()` (Harbor almost does).
4. Dual Badge (`ux_app.html` vs `ux_dom.ui`) — already on OWNERSHIP_COUNCIL.

---

## 8. Seat arguments (compressed)

**Law.** A fifth package is a third owner. Isolation already has a door
(`adapter/**`). Use it.

**Channel.** `applyOp` is immortal. Teaching it `transition.*` couples
the wire to a droppable peer. Peel-and-play after authority morph is the
only order that keeps images mounted.

**Document.** `document.use` is the contribution slot. MotionChannel
belongs there, next to `Motion()` and `XElement()`. Document does not
fold Ops.

**Motion.** The hook is 40 lines of JS and must not import Channel.
Owner in `name="ux_motion.channel"`. Player `applyOp("morph")` must use
`injectHtml`, not `innerHTML`, or identified images remount even when
the Host did everything right.

**Author.** Day-1 is still `update` / `notify` / `go`. Hosts that emit a
live `ops[]` import the adapter explicitly. That friction is intentional.

**Adversary.** `reply()`, `glue.js`, `ux-surface`, dual Button, a kit
package — each is a synonym or a second system. Kill on sight.

**Host.** `#view` and pantry are layout. Toast TTL is product feel.
One shop does not write Channel policy.

---

## 9. How to change this later

A future patch is legal only if the north star still holds **and** a
reopen condition below fires. If you cannot cite one, write a new
council entry first — do not “just refactor.”

### Reopen conditions

| You want to… | Legal when | Still illegal |
|---|---|---|
| Add a fifth package | Never. Promote into an existing core or this adapter. | `ux-kit`, `ux-paint`, `ux-glue` |
| Teach Channel `transition.*` | Never. Motion must stay droppable. | Op-table pollution |
| Promote Host chrome (toast TTL, img src pin, `#view`) | **3+ independent Hosts** share the *same* policy | One shop’s habit |
| Export `compose` / `lower_morph` on `ux_app.__all__` | `App.boot` authors need the wire more often than `update` | Dual author vocabulary on day-1 |
| Mint `ux_channel_ux_motion` as a repo | The hook grows a **Python** interop surface (not 40 lines of JS) | Package for a contribution |
| Revive `reply(*effects)` | Never. Banned name + second finish API. | Surface nostalgia |
| Put JS in `ux_app.adapter` | Never. Adapter is the Python import wall. | Mixing planes |
| Merge `id=` with `data-channel-id` | Never. Visual ≠ trust. | Cap / morph collision |
| Move XOR into Channel | Channel would have to parse motion plans | Channel learns `transition.*` |
| Harbor-isolate a Host (`@ch.on` → `App.boot`) | That Host’s product rewrite, not a library bump | Scope-bleed into 0.3.x |

### Reviewer questions (all six)

1. Which seat owns this truth **today**?
2. Does the change create a **second owner**?
3. Does it invent a synonym for Glue / Bridge / Adapter / Contribution?
4. Can Motion still be dropped? Can Channel still be dropped?
5. Does cold `import ux_app` still load no Channel / CEK?
6. Is this one Host habit, or three independent Hosts?

If any answer is “second owner” / “synonym” / “cannot drop” / “one Host”
— refuse. Record the refusal here, do not leave it in a chat.

### Failure modes this release closed

- Host compositor used a **taken** reserved word (`glue`).
- Dual remount: Channel idiomorph then motion `innerHTML` on the same target.
- Every Host copied `{op: morph, morph: idiomorph}`.
- Folding Scenes by hand (`ch.ui.op(*scene.play()["ops"])`) had no XOR check.

---

## 10. Verdict

**Approved under halt-or-patch.**

The stack was already in the right *order*. The mess was crossings sitting
in the shop under a taken name. They now live in the adapter and in a
named contribution. No fifth kernel. No revived predecessor.

Superseding this file requires a new `docs/` council entry that cites a
§9 reopen condition and the six reviewer answers.

**End of council record.**
