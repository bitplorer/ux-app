# Council — how the plan is executed

Agents sit as a **council**, not a pipeline of silent implementers.
The plan in [PLAN.md](PLAN.md) is the sequence. This file is the
procedure. Prompts are **artifacts**: when a corner is found, the
artifact that failed to prevent it is rewritten in the same turn.

Inspired by [META_PRODUCT_LIBRARY.md](META_PRODUCT_LIBRARY.md):
ingest live law before speaking, one concept one name, live file
wins, kill criteria halt, no leftover public language.

This is **not** a website. The council builds a library.

---

## 1. Strategy the council locks

**Prompt-as-artifact, halt-or-patch.**

```text
phase brief  →  implement  →  council gate
                    │
                    ├─ pass          → stamp the phase, advance
                    ├─ kill hit      → halt. fix code + test + artifact
                    ├─ live disagree → live file wins. Scribe patches
                    └─ weak corner   → fix now. log it. strengthen brief
```

Why this, not “just implement PLAN.md top to bottom”:

| Alternative | Why rejected |
|-------------|--------------|
| One implementer, no review | Leftover names and pair-identity bugs ship |
| Review only at the end | Isolation and Cap refuse are too late to unwind |
| Rewrite the plan after every wobble | Phases 0–7 stay; only *briefs* and *corners* move |
| Spawn a new prompt file per failure | Prompt sprawl. Patch in place (META rule) |

The plan is stable. The **briefs, corners log, and tests** are the
parts that get stronger under stress. That is the antifragile bit.

---

## 2. Seats

Six voting seats plus a clerk. One agent may hold one seat per
gate. Do not collapse Law into Author.

| Seat | Job | Veto |
|------|-----|------|
| **Law** | Frozen CEK words. K1–K10 as they apply to L7. Pair identity. Host decides / Peer applies. Profile never grants Cap power | Yes — law and frozen vocabulary |
| **Channel** | Isolation. Only `adapter/**` imports `ux_channel` / `cek_*`. Caps minted with the args the handler will see. `cek = off \| adapt \| require`. Cold import | Yes — isolation and Cap path |
| **Document** | ux-dom `Component` / `ReactiveComponent` honored, not wrapped twice. Tailwind only. `create-app` layers on `uxdom`. No second CSS or View DSL | Yes — Document / scaffold fights |
| **Domain** | Any pack, same path: load → agree → stamp → driver. Doctor fails a stamped pair with no driver. Rust Peer kernel = S only | Yes — undeclared pairs, missing drivers |
| **Author** | Public names, small `__all__`, day-1 cart under 40 lines. No Intent / CapService / stamp / preview in the golden file | No veto. Proposes names; Law can reject |
| **Adversary** | Tries leftover names, Peer mint, money on client, `"1"` as qty, split-alias pairs, `cek=off` emitting undeclared pairs, `--yes` as force | Yes — any kill criterion it can demonstrate |
| **Scribe** (clerk) | Does not vote. Patches artifacts in place. Appends [CORNERS.md](CORNERS.md). Never creates a parallel prompt file | — |

Read before a gate (progressive, not all at once):

| Seat | Opens |
|------|--------|
| Law | `cek-model.md`, CEK `KILL-CRITERIA.md`, `CORE/06`, `META/04-naming-law.md` |
| Channel | Channel `START_HERE.md`, `SPEC/INVARIANTS.md`, `ux_channel/cek/*` |
| Document | ux-dom `DESIGN_CANON.md`, `Component` / `ReactiveComponent` |
| Domain | `domains.md`, `CATALOG_AUTHORITY_TARGET.md`, `domain.rs`, `DRIVERS.md` |
| Author | `author-api.md`, `vocabulary.md` |
| Adversary | `mistakes.md`, `quality.md`, [CORNERS.md](CORNERS.md) |
| Scribe | this file, [PLAN.md](PLAN.md), [BUILD_PRODUCT_LIBRARY.md](BUILD_PRODUCT_LIBRARY.md), [META_PRODUCT_LIBRARY.md](META_PRODUCT_LIBRARY.md) |

If a live bitplorer file disagrees with a skill file, **the live file
wins**. Scribe patches the skill / prompt in the same turn.

---

## 3. Gate protocol

Run a gate at the end of **every** phase in PLAN.md, including
Phase 0. Do not skip to “we will review later.”

### 3.1 Brief (before implement)

Scribe writes or refreshes `prompts/briefs/phase-N.md` from BUILD +
PLAN + the open corners for that phase. The brief is the artifact
the implementer follows. It must include:

- the phase exit from PLAN.md
- the seats that must pass
- known corners that apply (ids from CORNERS.md)
- banned names (do not repeat the full vocabulary; link it)

If the brief is missing, the implementer does not start.

### 3.2 Implement

One implementer. Follows the brief. Does not rename frozen words.
Does not invent a second result type. Does not start a website.

### 3.3 Review

Each required seat answers only:

```text
PASS | PATCH | HALT
one sentence why
artifact to patch (if PATCH)
test to add (if PATCH or HALT)
```

**Required seats per phase** are listed in PLAN.md. Unlisted seats
may still HALT on a kill they can demonstrate.

### 3.4 Decision

| Outcome | When | What happens |
|---------|------|----------------|
| **Advance** | Every required seat PASS, Adversary silent or PASS | Stamp the phase in PLAN.md (`[x]`). Keep the brief. |
| **Patch** | Weakness that is not a kill | Fix code. Add a test. Scribe patches the brief and, if the playbook was wrong, the skill / BUILD / PLAN. Append CORNERS.md. Re-run the same gate. |
| **Halt** | Any kill criterion, or Law / Channel / Domain / Adversary HALT | Stop the phase. Do not start the next. Same repairs as PATCH, then re-gate. |

Unanimity is not required for Advance. **Any single veto seat saying
HALT is enough to halt.** Author cannot override Law.

### 3.5 Prompt-as-artifact rules (Scribe)

1. Patch **in place**. Do not add `BUILD_PRODUCT_LIBRARY_v2.md`.
2. META is the factory. Re-run META only when the skill’s law or
   author API changes, then overwrite BUILD.
3. PLAN phase order (0–7) does not change unless Law + Domain both
   agree a phase is in the wrong place.
4. Every new corner gets: an id, the phase it bit, the artifact that
   should have caught it, the test that now catches it.
5. A corner that is only “noted” and not tested has not been absorbed.
6. Banned names never appear as public identifiers in a patched brief.

---

## 4. Antifragile loop

Stress is useful only if it leaves a scar in the artifacts.

```text
found a corner
    │
    ├─ 1. reproduce with a test (or a doctor check)
    ├─ 2. fix the code so the test passes
    ├─ 3. write the prevention into the brief / BUILD / skill
    ├─ 4. append CORNERS.md
    └─ 5. re-run the same phase gate
```

Examples of “weak or has corners → corrected while executing”:

| Kind of weakness | How the council uses it |
|------------------|-------------------------|
| Live Channel API moved | Live file wins. Adapter changes. Brief cites the new path. |
| `cek=off` has no stamp | Domain seat HALT. Adapter keeps a pair set anyway. Corner logged. |
| Author wants `toast()` | Adversary + Domain HALT. Macro lowers to legal pairs, or a real `notice` domain. |
| ReactiveComponent double-wrap | Document HALT. Honor `_ensure_init_chain`. Test added. |
| Doctor green, Peer kernel skips `search.hits` | Domain HALT. Doctor must require a runtime driver. |
| Brief told the implementer to “finish ux-surface” | Scribe deletes that sentence. META quality check failed; fix META. |

The library gets stricter. The prompts get shorter and more precise.
The plan does not grow new phases for every scare.

---

## 5. What the council is not

- Not a second product name.
- Not a place to revive chrome / arm / reply / Effect.
- Not a design-by-committee of public APIs. Author proposes; Law
  and Domain constrain; Adversary tries to break.
- Not allowed to add React / TypeScript, a website, or a competing
  Channel.

---

## 6. How a run starts

1. Open this file and [PLAN.md](PLAN.md).
2. Scribe confirms CORNERS.md exists (pre-mortem already seeded).
3. Council confirms strategy still **halt-or-patch** (this section 1).
   Changing strategy is a charter change — all veto seats must agree.
4. Phase 0 brief → implement → gate. Then 1…7.
5. Done only when Phase 7 gate Advances and day-1 acceptance in
   BUILD is true.

Hand an implementer **BUILD + the current phase brief**, not this
whole council file. The implementer writes code. The council gates.
The Scribe keeps the artifacts honest.
