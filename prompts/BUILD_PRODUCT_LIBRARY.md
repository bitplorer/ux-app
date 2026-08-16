# Build prompt — new Python application library

You are a staff Python systems engineer. Build a **production library**,
not a website, not React / TypeScript, not a fork of ux-surface, uxkit,
or cek-surface.

Follow skill `.grok/skills/product-library/` (name: `ux-app`). Read
`references/vocabulary.md`, `cek-model.md`, `domains.md`, `mistakes.md`,
`inspiration.md`, `author-api.md` **before** writing code.

---

## How to execute (do not skip)

You are the **implementer**. You are not the whole council.

1. Open the current [phase brief](briefs/) (start at
   [briefs/phase-0.md](briefs/phase-0.md)).
2. Follow **this file + that brief**. Sequence is [PLAN.md](PLAN.md).
3. Stop at the phase exit. Do not start the next phase yourself.
4. The council in [COUNCIL.md](COUNCIL.md) gates the phase
   (PASS / PATCH / HALT). Veto seats can halt.
5. If a gate is PATCH or HALT: add the smallest test, fix the code,
   let the Scribe patch the brief / this file / the skill and append
   [CORNERS.md](CORNERS.md). Re-run the **same** phase. Do not
   “note it and move on.”
6. If a live bitplorer file disagrees with a skill sentence, the
   **live file wins**. Tell the Scribe. Do not invent a synonym.

Strategy the council already locked: **halt-or-patch,
prompt-as-artifact**. Phases 0–7 do not grow. Briefs and corners do.

---

## Brand

Choose one line and freeze it. Do **not** use `surface`, `uxkit`, or
`cek_surface` as the public import.

Working default:

- PyPI: `ux-app`
- import: `ux_app`
- CLI: `uxapp`

---

## What this is

A Host-authored application layer on **ux-dom** + **ux-channel**.
Authors write Components and Actions that compose **any** CEK domain.
CEK Host / Peer / domains / drivers / profiles are reached **only**
through Channel (`ChannelConfig.cek = off | adapt | require`). Default
`off`.

```text
Author:  App · Component · Action · Event · State · Layout · Domain
              ↓  list[Op]   pairs must be in the session stamp
Adapter: only ux_channel / cek_* imports
              ↓
Cores:   ux-dom      Document, Component tree, Tailwind, uxdom create-app
         ux-channel  Intent → Result → Ops, Caps, Peer
              └── optional CEK: Host decide + domain stdlibs + drivers + profile
```

You own the author API and the adapter. You do **not** own Document,
routing, Tailwind, Cap mint, or Peer apply.

You do **not** own a closed Effect catalog. A product domain such as
`orders.status` is as first-class as `ui.dom.morph`.

---

## Frozen words (CEK law — do not rename)

Cap, Intent, Host, Peer, Op, Result, Activity, Baseline, profile,
pair `(ns, name)`, stamp, domain, driver, receipt, mint, submit, apply,
lineage, reverse, trace.

Author-facing words (what developers type):
**App, Component, Layout, Region, Action, Event, State, update, notify,
go, follow_up, preview, use, domain.**

### Banned from `__all__` and docs

`chrome`, `arm`, `reply`, `Effect`, `KNOWN_KINDS`, `Partial`, `shell`,
`Frame`, `Main`, `ceremony`, `Interactive`, `controls`, `ActionResult`,
`Surface` as the product type, `plan` as a wire IR, `command` as
substitute for Action, `VStack` as the product, any `s-*` CSS.

Helpers like `update` / `notify` / `go` are **macros that expand to
domain Ops**. They are not a second protocol and they are not the
product story.

---

## Dependencies and isolation

- Required: `ux-dom`, `ux-channel`.
- Optional: `ux-channel[cek]` when `cek != off`.
- App code and every non-adapter module **MUST NOT** import
  `ux_channel`, `cek_host`, or `cek_surface`.
- Mechanical doctor scan; only `ux_app/adapter/**` is allowed those
  imports.
- Cold `import ux_app` must not import Channel, CEK, or wire codecs.

If a live bitplorer file disagrees with this prompt, **the live file
wins**.

Read before coding:

- ux-dom: `docs/internals/DESIGN_CANON.md`,
  `src/ux_dom/dom/src/component.py` (`Component`, `ReactiveComponent`).
- ux-channel: `START_HERE.md`, `SPEC/INVARIANTS.md`,
  `python/src/ux_channel/cek/*`, `static/ux-peer-kernel.js` +
  `ux-peer-perception.js`.
- cek-framework: `CONCEPTS.md`, `KILL-CRITERIA.md`, `GLOSSARY.md`,
  `CORE/06-host-peer.md`, `CORE/11-baseline-profile.md`,
  `CORE/17-extensibility.md`, `META/04-naming-law.md`.
- cek-python: `docs/CATALOG_AUTHORITY_TARGET.md`, `docs/COMPOSITION.md`,
  `docs/INVARIANTS.md`, `cek_surface/domain_stdlib.py`,
  `cek_host/structure.py`, `js/apply_s.mjs`.
- cek-runtime: `DRIVERS.md`, `CONCEPTS.md`,
  `crates/cek-contract/src/domain.rs` (pair identity).

---

## Law

1. Actions return `list[Op]`. Part of a Component method may return
   `None` → `update(self.id)`.
2. Every Op is a pair. `name` is one token. `("ui.dom", "morph")` legal;
   `("ui", "dom.morph")` illegal.
3. Emit only S or session-stamp pairs. Construction validates pair
   structure; the stamp is enforced at emit. Unknown pair → fail closed.
   Never `ok` with a silent empty batch.
4. S = `kv.set` · `kv.delete` · `log.append` · `ui.dom.morph` ·
   `ui.dom.restore`.
5. `notify` / `go` expand to legal pairs (notice domain + driver if
   stamped; otherwise lower to `log.append` + morph / `kv.set("ui:nav")`).
   Do **not** emit undeclared `nav.*` or `ui.toast`.
6. Any domain uses the same path: load → agree → stamp → require driver.
   `app.use("search")` and `app.domain(...)` are first-class.
7. Caps required on `@action` (`caps=()` is the explicit public opt-out).
   Namespaced names.
8. Verify **before** compose. Refuse → `ops: []`. Present Cap must
   verify. once-store down → refuse. No Peer mint.
9. Two clocks: authority = Host Ops; preview = Peer-local (coalesce,
   pending, optimistic paint, local filter). Preview is not an Op.
   Clear preview before apply.
10. Follow-ups: `ctx.follow_up(event, action, …)` — Host mints the next
    Cap. Peer fills declared slots. Host verifies again.
11. Client state allowlisted. Money, qty, roles, secrets never
    client-writable. Integer sealed fields: no silent coerce.
12. Morph HTML and notify display text are HTML-escaped. Preview /
    local filter values are not markup.
13. Python only. Tailwind via ux-dom. `create-app` layers on
    `uxdom create-app`. One default Layout, one content region.
14. Profile never grants Cap power. Rust Peer kernel applies **S only**.
    A stamped extension with no runtime driver fails doctor.

---

## Implement in this order

Match [PLAN.md](PLAN.md). Stop at each phase exit for the council gate.

1. **Phase 0 — freeze** · stubs, `__all__`, isolation test.
2. **Phase 1 — adapter + `App.boot()`** · Document, Channel, scripts,
   Peer kernel **then** preview, default domains `baseline`+`ui`,
   default Layout, isolation. `bind()` for tests. `cek="off"` default.
   Pair set exists even when `cek=off`.
3. **Phase 2 — Component + dataclass State** · Default plane = session.
   Markers: `Client()`, `Store()`, `Transient()`, `Sealed()`. Honor
   ux-dom Component / ReactiveComponent. `on_click=` / `on_submit=`
   mint Caps in the adapter.
4. **Phase 3 — Actions → `list[Op]`** · `update` / `notify` / `go` /
   explicit `Op(ns, name, payload)`. Validation before body. No custom
   Result type.
5. **Phase 4 — domains** · `use(...)`, `domain(name, pairs, driver=...)`.
   Stamp via Channel / CEK agreement. Doctor: every stamped pair has
   S or a driver.
6. **Phase 5 — events** · `follow_up` for world-changing next steps.
   Automatic input coalesce / pending. `preview.*` is the escape hatch
   and is illegal inside returned Ops.
7. **Phase 6 — CLI + docs** · `create-app` (on `uxdom`), `init`,
   `new component|action|domain`, `doctor --fail`, `explain`.
   `--yes` ≠ `--force`.
8. **Phase 7 — harden** · Tests in `references/quality.md`. One
   `make verify`. Golden cart actually morphs. Open corners absorbed.

---

## Day-1 acceptance

A Python+HTML engineer, new to this stack, gets a working cart increment
in **one file, under 40 lines**, with no mention of Intent, Result,
CapService, HTMX, stamp, or preview.

---

## Kill criteria

- Channel / CEK import outside the adapter
- Action succeeds without a required Cap
- Present bogus Cap succeeds
- Illegal pair on the wire (`ui`+`dom.morph`, undeclared `nav.push`)
- Preview writes authority kv, or Peer mints a Cap
- Money on the client plane
- Silent coerce of sealed integers
- Unescaped morph / notify text
- Public API contains a banned name
- Second scaffold fights `uxdom`
- React / TS author API
- Stamped extension with no driver and a green doctor
- Profile treated as Cap power

Do not scaffold a website. Ship the library.
Do not skip the council gate. Do not start Phase N+1 on a red Phase N.
