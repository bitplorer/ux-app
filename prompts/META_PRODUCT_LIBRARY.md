# Meta-prompt — generate an implementation prompt for the application library

You are a staff Python systems engineer and library designer. Your job
is to **write or refresh artifacts** (not the library, not a website)
that another engineer and a council of seats can follow.

Skill: `.grok/skills/product-library/` (name: `ux-app`).

This meta-prompt is the **factory**. It overwrites artifacts **in
place**. It does not accumulate `BUILD_v2.md`.

---

## What you emit (always these, nothing else)

| Artifact | Role | Rule |
|----------|------|------|
| [BUILD_PRODUCT_LIBRARY.md](BUILD_PRODUCT_LIBRARY.md) | Implementer contract | Overwrite in place when skill law or author API changes |
| [PLAN.md](PLAN.md) | Locked phases 0–7 | Phase **order** changes only if Law + Domain would agree |
| [COUNCIL.md](COUNCIL.md) | How seats gate a phase | Strategy stays halt-or-patch unless all veto seats would agree |
| [CORNERS.md](CORNERS.md) | Immune system | You may seed pre-mortem rows. You never delete found rows |
| [briefs/phase-N.md](briefs/) | Current-phase brief | Refresh from BUILD + PLAN + open corners |

Do not emit a website. Do not emit library source.

---

## What the product is

A **new** Host-authored Python application layer on **ux-dom** +
**ux-channel**. Authors write `App`, `Component`, `Action`, `Event`,
dataclass `State`, `Layout`. Actions return `list[Op]`. Any CEK
**domain** can join a session (load → agree → stamp → driver). CEK
Host / Peer / domains / drivers / profiles are reached **only** through
`ChannelConfig.cek = off | adapt | require`. Default `off`.

It is not a website. It is not React / TypeScript. It is not a fork of
`ux-surface`, `uxkit`, or `cek-surface`.

---

## Ingest before you write a word

Read, in this order. If a live bitplorer file disagrees with the skill,
**the live file wins**.

1. Skill: `.grok/skills/product-library/SKILL.md`
2. `.grok/skills/product-library/references/vocabulary.md`
3. `.grok/skills/product-library/references/cek-model.md`
4. `.grok/skills/product-library/references/domains.md`
5. `.grok/skills/product-library/references/mistakes.md`
6. `.grok/skills/product-library/references/inspiration.md`
7. `.grok/skills/product-library/references/author-api.md`
8. Existing [COUNCIL.md](COUNCIL.md), [PLAN.md](PLAN.md), [CORNERS.md](CORNERS.md)
9. Live law:
   - cek-framework `CONCEPTS.md`, `KILL-CRITERIA.md`, `CORE/06-host-peer.md`,
     `CORE/11-baseline-profile.md`, `CORE/17-extensibility.md`, `META/04-naming-law.md`
   - cek-runtime `CONCEPTS.md`, `DRIVERS.md`, `06-profiles/README.md`,
     `crates/cek-contract/src/domain.rs`
   - cek-python `docs/CATALOG_AUTHORITY_TARGET.md`, `docs/COMPOSITION.md`,
     `docs/INVARIANTS.md`, `cek_surface/domain_stdlib.py`, `cek_host/structure.py`
   - ux-channel `START_HERE.md`, `SPEC/INVARIANTS.md`, `python/src/ux_channel/cek/*`
   - ux-dom `docs/internals/DESIGN_CANON.md`, `Component` / `ReactiveComponent`

---

## Naming law you must enforce in every artifact

Names answer **intention**, not leftover conversation.

**Frozen (do not rename, do not synonym-fork):**
Cap, Intent, Host, Peer, Op, Result, Activity, Context, lineage, reverse,
trace, Baseline, profile, mint, submit, apply, pair `(ns, name)`, stamp,
domain, driver, receipt.

**Author-facing (what developers type):**
App, Component, Layout, Region, Action, Event, State,
update, notify, go, follow_up, preview, use, domain.

**Banned from public API, `__all__`, README examples, and type names:**
chrome, arm, reply, Effect, KNOWN_KINDS, Partial, shell, Frame, Main,
ceremony, Interactive, controls, ActionResult, Surface (as the product
type), plan (as a wire IR), command (as substitute for Action / Intent),
VStack as the product, any `s-*` CSS.

If you need a word, write the job in one sentence and pick a standard
developer word. Do not revive a banned name “just internally” if it will
leak.

---

## Council + antifragile rules the artifacts must encode

Take the method of this file (ingest → freeze names → emit a contract
→ quality check) and apply it **while the plan runs**:

1. Agents sit as seats: Law, Channel, Document, Domain, Author,
   Adversary, plus Scribe (clerk). See COUNCIL.md.
2. Strategy is **halt-or-patch**. Any veto seat saying HALT stops the
   phase. Weakness is absorbed the same turn: test + fix + patch
   artifact + CORNERS row → re-gate the **same** phase.
3. Prompts are artifacts. Patch in place. No versioned prompt files.
4. Pre-mortem corners are seeded before Phase 0. Found corners only
   append. A corner is not absorbed until it has a test.
5. Live file wins. Scribe patches the skill / BUILD / brief, not the
   author API into a synonym.
6. Domains stay first-class. Do not emit a plan that hides `app.use`
   / `app.domain` behind a closed catalog.

---

## Invariants the implementation prompt must encode

1. Actions return `list[Op]`. Helpers are macros that expand to legal pairs.
2. Pair identity: `name` is one token. `("ui.dom", "morph")` legal;
   `("ui", "dom.morph")` illegal.
3. Emit only S or session-stamp pairs. Unknown pair → fail closed.
4. S = `kv.set` · `kv.delete` · `log.append` · `ui.dom.morph` · `ui.dom.restore`.
5. Any domain uses the same path: load → agree → stamp → require driver.
6. Caps required on `@action` (`caps=()` is the explicit public opt-out).
7. Verify before compose. Refuse → `ops: []`. Present Cap must verify.
   once-store down → refuse. No Peer mint.
8. Two clocks: authority = Host Ops; preview = Peer-local. Preview is not
   an Op. Clear preview before apply.
9. Follow-ups: Host mints the next Cap. Peer fills declared slots.
10. Client state allowlisted. Money, qty, roles, secrets never client-writable.
11. Isolation: only `adapter/**` imports `ux_channel` or `cek_*`.
12. Python only. Tailwind via ux-dom. `create-app` layers on `uxdom create-app`.
13. Profile never grants Cap power. Rust Peer kernel applies S only;
    extensions need a Peer runtime driver.

---

## Shape of BUILD (the implementer contract)

Produce / refresh a single markdown file with these sections, in order:

1. **Role** — staff Python systems engineer; library, not website.
2. **Brand** — one frozen PyPI / import / CLI line.
3. **What this is / is not** — ownership diagram vs ux-dom / Channel / CEK.
4. **Vocabularies** — frozen vs author-facing vs banned.
5. **Dependencies and isolation.**
6. **Live-file-wins** + the exact files to read before coding.
7. **Law** — numbered invariants (including domains / drivers / profiles).
8. **How to execute** — point at PLAN + COUNCIL + current phase brief.
   Implementer follows BUILD + brief. Council gates. Scribe patches.
9. **Implement in this order** — adapter → Component/State → Actions →
   domains → events → CLI → docs/tests. Domains are not an afterthought.
10. **Day-1 acceptance** — one file, under 40 lines, cart morphs, no
    mention of Intent / CapService / stamp / preview.
11. **Kill criteria** — copied from the skill’s quality bar + CEK K1–K10
    as they apply to L7.

Do not include leftover names even as “we used to call this X.”
Do not ask the implementer to scaffold a website.
Do not ask the implementer to finish ux-surface or uxkit.

---

## Quality check before you hand artifacts over

- [ ] No banned name appears as a public identifier
- [ ] Domains / drivers / profiles / stamp are first-class, not a footnote
- [ ] CEK is reached only through Channel
- [ ] Author API matches `references/author-api.md`
- [ ] Tests listed in `references/quality.md` are required
- [ ] Live bitplorer paths are cited
- [ ] Brand is frozen to one line
- [ ] PLAN still has phases 0–7 and names required seats
- [ ] COUNCIL still says halt-or-patch, prompt-as-artifact
- [ ] CORNERS still has the pre-mortem; found rows were not deleted
- [ ] Current phase brief exists and cites its C-pre-* ids

The canonical implementation prompt this meta-prompt is meant to produce
is [BUILD_PRODUCT_LIBRARY.md](BUILD_PRODUCT_LIBRARY.md). Revise that file
in place when the skill changes; do not accumulate old prompt files.
