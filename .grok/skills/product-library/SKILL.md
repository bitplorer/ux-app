---
name: ux-app
description: >
  Author a new Python application library on ux-dom + ux-channel that
  reaches CEK Host, Peer, domains, drivers, and profiles only through
  Channel. Use when building a Host-authored layer: App, Component,
  Action, Event, dataclass State, Layout, and any domain Ops. Never a
  website. Never a fork of ux-surface or uxkit.
metadata:
  short-description: "New Python app layer: Components + Actions + any CEK domain"
user-invocable: true
---

# Application library (new — not a fork)

Build a **new** Python library. Take **ideas** from the bitplorer stack.
Do **not** reuse the public APIs, type names, or slogans of `ux-surface`,
`uxkit`, or `cek-surface`.

This skill produces a **library**. Never a website, SPA, or marketing page.

**Read on demand**

| File | When |
|------|------|
| [references/vocabulary.md](references/vocabulary.md) | Before naming anything |
| [references/cek-model.md](references/cek-model.md) | Host, Peer, domain, driver, profile, stamp |
| [references/domains.md](references/domains.md) | How any domain is declared, agreed, stamped, driven |
| [references/author-api.md](references/author-api.md) | Day-1 App, Component, Action, Event, State |
| [references/inspiration.md](references/inspiration.md) | What to take from each bitplorer library |
| [references/mistakes.md](references/mistakes.md) | What not to copy |
| [references/quality.md](references/quality.md) | Tests, doctor, docs, kill criteria |

**Action plan (council + sequence)**

| File | When |
|------|------|
| [prompts/COUNCIL.md](../../../prompts/COUNCIL.md) | How agents sit, vote, and patch artifacts |
| [prompts/PLAN.md](../../../prompts/PLAN.md) | Locked phases 0–7 (finalized) |
| [prompts/CORNERS.md](../../../prompts/CORNERS.md) | Pre-mortem + living weak-edge log |
| [prompts/briefs/](../../../prompts/briefs/) | Per-phase implementer briefs |
| [prompts/META_PRODUCT_LIBRARY.md](../../../prompts/META_PRODUCT_LIBRARY.md) | Factory that rewrites the build prompt |
| [prompts/BUILD_PRODUCT_LIBRARY.md](../../../prompts/BUILD_PRODUCT_LIBRARY.md) | Implementer contract |

Strategy: **halt-or-patch, prompt-as-artifact**. Phases stay.
Weakness found in flight → test + fix + patch the brief / BUILD /
skill + append CORNERS.md → re-run the **same** gate.

---

## 1. What you are building

A **Host-authored application layer**. Authors write Python. The Peer only applies Ops.

The product is **not** a closed UI-effect catalog. It is a way to write
Components and Actions that compose **any** CEK domain: `baseline`, `ui`,
`search`, or a product pack such as `orders` / `billing`.

```text
Author:  App · Component · Action · Event · State · Layout · Domain
              ↓  returns list[Op]   pairs must be in the session stamp
Adapter: only module that may import ux_channel / cek_*
              ↓
Cores:   ux-dom     Document, Component tree, Tailwind
         ux-channel Intent → Result → Ops, Caps, Peer attach
              └── ChannelConfig.cek = off | adapt | require
                    Host decide · domain stdlibs · drivers · profile
```

| Owns | Does not own |
|------|----------------|
| App façade, Components, Actions, Events, field State, Layouts | Document, routes, Tailwind (`ux-dom`) |
| Author helpers that **expand to domain Ops** | Cap mint / verify (`cek-host` / Channel) |
| Domain registration + driver wiring for the product | Peer kernel apply (`ux-peer-kernel` / `cek apply`) |
| Isolation so app code never imports Channel / CEK | A second wire protocol |

**Dependencies:** `ux-dom` + `ux-channel` required. CEK only through
`ChannelConfig.cek = off | adapt | require`. Default `off`.

**Brand (freeze one line):** PyPI `ux-app` · import `ux_app` · CLI `uxapp`.
Do not reuse `surface`, `uxkit`, or `cek_surface` as the public import.

---

## 2. Two vocabularies (do not mix)

**Frozen CEK words** — law. Synonym-forking them is a kill (K10). Use them
only with their real meanings:

Cap · Intent · Host · Peer · Op / Ops · Result · Activity · Context ·
lineage · reverse · trace · Baseline · profile · mint · submit · apply ·
pair `(ns, name)` · stamp · domain · driver · receipt

**Author-facing words** — what developers type. They map **onto** the
frozen words in the adapter; they never replace them:

App · Component · Layout · Region · Action · Event · State ·
update · notify · go · follow_up · preview · use · domain

Naming method and banned leftover names: [vocabulary.md](references/vocabulary.md).

---

## 3. Loop (do not skip)

1. Read `vocabulary.md` + `cek-model.md` + `domains.md` + `mistakes.md`.
2. Confirm council strategy in `prompts/COUNCIL.md` (halt-or-patch).
3. Freeze brand + a small public `__all__` (Phase 0 brief).
4. For each phase 0–7: refresh the brief → implement → council gate.
5. On PATCH/HALT: test + fix + patch artifacts + log the corner.
   Do not start the next phase on a red gate.
6. Isolation scan + doctor stay green from Phase 1 on.
7. Tests against **real** Channel / CEK contracts.
8. One golden app: one file, under 40 lines, cart increment morphs. No website.

If a live bitplorer file disagrees with this skill, **the live file wins**.
Scribe patches this skill in the same turn.

---

## 4. Hard rules

1. App code and every non-adapter module **must not** import `ux_channel`,
   `cek_host`, or `cek_surface`.
2. Actions return `list[Op]` (or a helper that **is** a list of Ops).
   No second result type (`reply`, `ActionResult`, `Effect`).
3. Every Op is a **pair** `(ns, name)` with `name` one token.
   `("ui.dom", "morph")` is legal; `("ui", "dom.morph")` is not.
4. Emit only pairs in **S** or in the **session stamp**. Unknown pair →
   fail closed. Never `ok` with a silent empty batch.
5. Verify Cap **before** compose. Refuse → `ops: []`. Present Cap must
   verify. once-store down → refuse.
6. Peer never mints. Peer never writes authority kv as truth.
   Profile never grants Cap power.
7. Preview (pending, optimistic paint, input coalesce) is **Peer-local**.
   It is not an Op. It must clear before apply.
8. Control flow stays on the Host: follow-up Actions are Host-issued
   (pre-minted Cap + template). Peer fills declared slots only.
9. Python only. No React / TS author API. Tailwind via ux-dom.
   No parallel CSS framework.
10. Money, quantity, roles, secrets: never client-writable state.
11. A stamped pair with no driver fails doctor. The Rust Peer kernel
    applies **S only**; extensions need a Peer **runtime** driver.

---

## 5. What “done” means

- `App.boot()` stands up Document + Channel + default domains
  (`baseline`, `ui`) + Peer apply + preview attach.
- A dataclass Component field is session state unless marked otherwise.
- `app.use("search")` loads the stdlib, agrees with the Peer, stamps
  pairs, and requires a driver or fails doctor.
- `app.domain(...)` registers a product domain the same way.
- Golden cart morphs. Isolation doctor is green.
- Public `__all__` contains no leftover names.
- Phase 7 council gate Advanced. Open pre-mortem corners are
  absorbed or an explicit `wont`.

Do not implement until handed [BUILD_PRODUCT_LIBRARY.md](../../../prompts/BUILD_PRODUCT_LIBRARY.md)
and the current [phase brief](../../../prompts/briefs/).
This skill is the playbook. The build prompt is the implementer contract.
The council is how the plan stays correct while it runs.
