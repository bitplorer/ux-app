# Phase 0 brief — freeze

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 0.
Procedure: [COUNCIL.md](../COUNCIL.md).
Skill: `.grok/skills/product-library/`.

**Required seats at the gate:** Law, Author, Adversary, Scribe.

This phase writes **stubs and contracts**, not behavior.

---

## Do

1. Freeze brand: PyPI `ux-app` · import `ux_app` · CLI `uxapp`.
2. Create the package tree in PLAN.md Phase 0. Adapter folder exists
   even if files are empty except for docstrings.
3. Draft a small public `__all__`:
   `App`, `Component`, `action`, `update`, `notify`, `go`, `Op`,
   `follow_up`, `preview`, `Client`, `Store`, `Transient`, `Sealed`.
4. `pyproject.toml`: depends on `ux-dom`, `ux-channel`. Optional
   `[cek]` extra → `ux-channel[cek]`.
5. Isolation unit test from day one: importing `ux_channel` or
   `cek_*` from any module outside `ux_app/adapter/` fails.
6. Cold-import test: `import ux_app` does not import Channel, CEK,
   or wire codecs (may xfail until Phase 1 if the adapter is empty —
   do not “fix” it by importing cores at package root).

---

## Do not

- Implement boot, Actions, or domains yet.
- Copy `src/surface/**` or uxkit.
- Put leftover names in the tree (`chrome`, `arm`, `reply`, `Effect`,
  `Partial`, `shell`, `Surface` as a type, `command` as Action).
- Scaffold a website or start a preview server.

---

## Corners this brief must not miss

C-pre-01 brand collision · C-pre-02 banned names in `__all__` ·
C-pre-03 cold import.

---

## Exit

Layout exists. `__all__` scan is green. Isolation test is real
(fails if a non-adapter module imports Channel). Council gate
before Phase 1.
