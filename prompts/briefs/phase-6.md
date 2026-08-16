# Phase 6 brief — CLI + docs

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 6.

**Required seats:** Document, Author, Adversary.

---

## Do

1. `uxapp create-app` layers on `uxdom create-app` when that CLI is
   on PATH. Otherwise writes the App layer only.
2. `init`, `new component|action|domain`, `doctor --fail`, `explain`.
3. `--yes` is not `--force`. Existing files are skipped unless `--force`.
4. Docs: `README.md`, `START.md`, `ARCHITECTURE.md`, `DOMAINS.md`,
   `docs/AGENTS.md` (workspace root `AGENTS.md` is the sandbox agent
   file; the library maintainer map lives under `docs/`).
5. `py.typed`. `make verify` runs tests + isolation + public scan + doctor.

## Corners

C-pre-29, C-pre-30.

## Exit

A new engineer follows `START.md` to a morphing cart. `explain` dumps
Actions, Components, domains, stamp, drivers.
