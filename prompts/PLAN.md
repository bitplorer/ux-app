# Finalized plan

This is the **locked sequence** for building `ux-app`.
The council in [COUNCIL.md](COUNCIL.md) executes it.
The implementer brief is [BUILD_PRODUCT_LIBRARY.md](BUILD_PRODUCT_LIBRARY.md).
The factory that rewrites that brief is [META_PRODUCT_LIBRARY.md](META_PRODUCT_LIBRARY.md).
Known weak edges live in [CORNERS.md](CORNERS.md).

Skill: `.grok/skills/product-library/` (name: `ux-app`).

Do not start from ux-surface or uxkit source.
Do not scaffold a website.

---

## Council decision (strategy)

The seats sat against this plan and locked **halt-or-patch,
prompt-as-artifact**:

1. Phases **0–7 stay**. We do not invent Phase 8 for every scare.
2. Every phase has a **brief** (`prompts/briefs/phase-N.md`) derived
   from BUILD + this file + the open corners that apply.
3. Every phase ends in a **council gate**. Veto seats can halt.
4. A weakness found in flight is absorbed the same turn: test +
   code fix + artifact patch + CORNERS.md row. Then the **same**
   gate re-runs.
5. Live bitplorer files beat this plan. Scribe patches the plan
   sentence that was wrong; the phase order only moves if Law and
   Domain both agree.

Rejected alternatives (so we do not revisit them mid-run):

- “Implement everything, review at the end” — isolation and Cap
  refuse cannot be retrofitted cheaply.
- “New prompt file per failure” — sprawl. Patch BUILD / briefs
  in place.
- “Domains as a later add-on” — that is the ux-surface mistake.
  Domain path is first-class from Phase 0 (default `{baseline, ui}`)
  and has its own Phase 4 for extension.

---

## How a phase is run

```text
Scribe:  refresh prompts/briefs/phase-N.md
         (BUILD + this phase + open C-pre-* / C-### for N)
Implementer: follow the brief only
Council: each required seat → PASS | PATCH | HALT
Scribe:  on PATCH/HALT → test + fix + patch artifact + log corner
         on all required PASS → mark the phase [x] and advance
```

Hand the implementer **BUILD + the phase brief**, not the whole
council file.

---

## Phase 0 — freeze

**Required seats:** Law, Author, Adversary, Scribe.

- [x] Brand: PyPI `ux-app` · import `ux_app` · CLI `uxapp`
- [x] Public `__all__` drafted (small). No banned names.
- [x] Package layout:

```text
src/ux_app/
  __init__.py          # App, Component, action, update, notify, go, Op
  app.py
  component.py
  action.py
  state.py
  events.py
  domains.py           # use(), domain(), pair set, doctor hooks
  preview.py           # Peer-local escape hatch; not Ops
  layout.py
  adapter/             # ONLY place ux_channel / cek_* may be imported
    boot.py
    channel.py
    document.py
    caps.py
    peer.py
    cek.py             # thin wrap of ux_channel.cek; empty when cek=off
  cli/
  py.typed
```

- [x] `pyproject.toml` depends on `ux-dom` + `ux-channel`. Optional
      extra `[cek]` → `ux-channel[cek]`.
- [x] Isolation scan wired as a unit test from day one.
- [x] `prompts/briefs/phase-0.md` exists. CORNERS.md pre-mortem cited
      (C-pre-01, C-pre-02, C-pre-03).

**Exit:** layout exists, `__all__` scan is green, isolation test
fails if a non-adapter module imports Channel. No product code
needed beyond stubs.

**Gate question:** would a new engineer infer leftover names from
the tree? If yes → Author PATCH.

---

## Phase 1 — adapter + boot

**Required seats:** Channel, Document, Domain, Adversary.

Stand up cores. No author sugar yet.

- [x] `App.boot(title=..., cek="off")` creates Document + Channel,
      injects scripts, attaches Peer kernel **then** preview.
- [x] Default domains `{baseline, ui}` → session pair set = S.
- [x] Default Layout, one content region.
- [x] `App.bind(document=..., channel=...)` for tests.
- [x] Isolation doctor runs at boot when strict.
- [x] Cold `import ux_app` does not import Channel / CEK / codecs.
- [x] `cek=off` still refuses undeclared pairs (C-pre-06).

**Corners to hold:** C-pre-03 … C-pre-07, C-pre-34.

**Exit:** a test boots App, renders an empty page with scripts
present, doctor green, pair set = S.

---

## Phase 2 — Component + State

**Required seats:** Document, Author, Channel, Adversary.

- [x] A class with `id` + `render` is a Component. Honor ux-dom
      `Component` / `ReactiveComponent` if subclassed.
- [x] Dataclass fields default to session. Markers: `Client()`,
      `Store()`, `Transient()`, `Sealed()`.
- [x] Client keys must be on the allowlist. Money-shaped names on
      client fail doctor.
- [x] `on_click=` / `on_submit=` mint Caps in the adapter with the
      args the handler will see.
- [x] Optional field validators (valio-style or plain). No silent
      coerce of sealed ints.

**Corners to hold:** C-pre-08 … C-pre-11.

**Exit:** render a badge Component; click path exists; Cap is
present on the control.

---

## Phase 3 — Actions → list[Op]

**Required seats:** Law, Channel, Domain, Adversary.

- [x] `@action("orders.create", caps=[...])`. `caps=()` is explicit
      public opt-out.
- [x] Return `list[Op]`. Component method `None` → `update(self.id)`.
- [x] Macros: `update` → `ui.dom.morph`; `notify` / `go` lower to
      legal pairs only.
- [x] `Op(ns, name, payload)` fails closed if the pair is not in S
      or the session stamp.
- [x] Verify before compose. Refuse → `ops: []`. Present Cap verifies.

**Corners to hold:** C-pre-12 … C-pre-17, C-pre-13 especially.

**Exit:** golden cart — click increments, morph 0→1, refuse-without-cap
leaves the world unchanged.

---

## Phase 4 — domains (first-class)

**Required seats:** Domain, Law, Channel, Adversary.

This is the product, not an add-on.

- [x] `app.use("search")` loads bundled stdlib, agrees, stamps,
      requires driver.
- [x] `app.domain(name, version, pairs, driver=...)` for product packs.
- [x] Structure validation (`validate_pair` rules).
- [x] Doctor: every stamped pair is S or has a driver.
- [x] Pair-identity tests: `("ui.dom","morph")` ok;
      `("ui","dom.morph")` illegal.
- [x] When `cek=require`, handshake goes through Channel’s CEK adapter.
      When `cek=off`, the adapter still maintains a pair set.

**Corners to hold:** C-pre-18 … C-pre-23, C-pre-19 especially
(Rust Peer kernel applies S only).

**Exit:** `use("search")` without a driver fails doctor; with a
driver, `Op("search","hits",…)` applies. A custom `orders.status`
domain works the same way.

---

## Phase 5 — events + preview

**Required seats:** Law, Domain, Author, Adversary.

- [x] `ctx.follow_up(event, action, args_from=...)` mints a
      continuation Cap on the Host.
- [x] Peer fills declared slots only. Host verifies again.
- [x] Bound inputs automatically coalesce / pending (Peer preview).
- [x] `preview.pending` / `preview.update` / `preview.filter` exist
      as escape hatches and are illegal inside returned Ops.
- [x] Next Result clears preview, then applies Ops.

**Corners to hold:** C-pre-24 … C-pre-28, C-pre-33 (do not
re-export sibling leftover verbs).

**Exit:** debounce-style search type → follow-up commit; preview
gone after Result; Peer cannot fire the follow-up without the Host Cap.

---

## Phase 6 — CLI + docs

**Required seats:** Document, Author, Adversary.

- [x] `uxapp create-app` layers on `uxdom create-app`.
- [x] `init`, `new component|action|domain`, `doctor --fail`, `explain`.
- [x] `--yes` is not `--force`.
- [x] Docs: `README.md`, `START.md`, `ARCHITECTURE.md`, `DOMAINS.md`,
      `AGENTS.md`.
- [x] `py.typed`. `make verify` runs tests + isolation + doctor.

**Corners to hold:** C-pre-29, C-pre-30.

**Exit:** a new engineer follows `START.md` to a morphing cart.
`explain` dumps Actions, Components, domains, stamp, drivers.

---

## Phase 7 — harden

**Required seats:** all six voting seats.

- [x] All tests in `references/quality.md`.
- [x] Public `__all__` scanned for banned names.
- [x] production profile: durable once-store, receipts on.
- [x] Async Action: sync submit refuses; `async_submit` runs it.
- [x] No leftover names in docs or examples.
- [x] Every `open` pre-mortem corner is `absorbed` or an explicit
      `wont` with a live-file citation.
- [x] Day-1 acceptance in BUILD is true (one file, <40 lines, cart
      morphs, no Intent / CapService / stamp / preview).

**Corners to hold:** C-pre-31, C-pre-32, and every execution row
in CORNERS.md.

**Done** when this gate Advances.

---

## If something is weak mid-flight

Do not fork the plan. Do this, in order:

1. Adversary (or the seat that saw it) writes the smallest
   reproducing test or doctor check.
2. Implementer fixes the code.
3. Scribe adds a CORNERS.md row and one sentence to the phase
   brief (and to BUILD / skill if the playbook was wrong).
4. Re-run **this** phase gate. Do not start the next phase on a
   red gate.

If the live Channel / CEK API moved: live file wins, adapter
changes, brief cites the new path. The author API does not grow
a synonym to paper over it.

---

## What “final” means

This file is the sequence. [COUNCIL.md](COUNCIL.md) is the
procedure. [CORNERS.md](CORNERS.md) is allowed to grow.
[BUILD_PRODUCT_LIBRARY.md](BUILD_PRODUCT_LIBRARY.md) is patched
in place when META is re-run. Phase order changes only under
Law + Domain agreement.

The library is not started until Phase 0’s brief exists and the
council confirms the strategy above still holds.

---

## Council gates (this run)

Strategy confirmed: halt-or-patch, prompt-as-artifact. Phases 0–7
did not grow. Weak edges found in flight were absorbed the same
turn (C-001 … C-004).

| Phase | Seats | Decision | Note |
|-------|-------|----------|------|
| 0 | Law, Author, Adversary, Scribe | Advance | Brand `ux-app` / `ux_app` / `uxapp`. No leftover tree names. Isolation test is real. |
| 1 | Channel, Document, Domain, Adversary | Advance | `boot`/`bind`, scripts kernel-then-preview, pair set = S even when `cek=off`. LocalRuntime is not a third kernel. |
| 2 | Document, Author, Channel, Adversary | Advance | Duck-type Component. Sealed ints refuse coerce. Caps minted with handler defaults. |
| 3 | Law, Channel, Domain, Adversary | Advance | Golden cart 0→1. Refuse → `ops: []`. Present Cap verifies. |
| 4 | Domain, Law, Channel, Adversary | Advance | `use("search")` doctor-red without driver. Product `orders.status` same path. |
| 5 | Law, Domain, Author, Adversary | Advance | Follow-up needs Host Cap. Preview cleared after Result. Preview is not an Op. |
| 6 | Document, Author, Adversary | Advance | CLI layers on `uxdom`. `--yes` ≠ `--force`. Docs shipped. Library maintainer map at `docs/AGENTS.md` (C-002). |
| 7 | all six | Advance | `make verify` green. 65 tests. Day-1 cart is 14 non-empty lines. Open pre-mortem corners absorbed or `wont`. |

Phase 7 gate **Advances**. The library is done.

