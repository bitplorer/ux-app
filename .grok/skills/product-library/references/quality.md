# Quality bar

## Docs (ship with the library)

| File | Job |
|------|-----|
| `README.md` | One-file cart. Install. What it is / is not. |
| `START.md` | First morph in 5 minutes. |
| `ARCHITECTURE.md` | Ownership vs ux-dom / Channel / CEK. Adapter boundary. |
| `DOMAINS.md` | How to add a domain + driver. Pair identity. Stamp. Profile. |
| `AGENTS.md` | Maintainer map. Generators vs hand-written. |

No synonym glossary. Link CEK CONCEPTS for Cap / Host / Peer / Op.

## Tests (must exist)

1. Isolation: importing Channel / CEK outside `adapter/` fails doctor.
2. Cap refuse → `ops == []` and world unchanged.
3. Present bogus Cap on a public Action still verifies and refuses.
4. Sealed qty as `"1"` is rejected (no coerce).
5. Pair identity: `("ui.dom", "morph")` applies; `("ui", "dom.morph")` is illegal.
6. `app.use("search")` without a search driver fails doctor.
7. Product `app.domain(...)` pair is illegal on the wire before `use` / register.
8. Follow-up Action: Peer cannot run it without the Host-issued Cap.
9. Preview pending / optimistic paint is gone after the next Result.
10. Dataclass field default plane is session; `Client()` key not on allowlist raises.
11. Money-shaped field marked client fails doctor / type gate.
12. Async Action: sync submit refuses; `async_submit` runs it (no nested loop).
13. Golden cart: click → morph count 0→1.
14. Public `__all__` contains none of the banned names in vocabulary.md.

Prefer Channel / CEK contract vectors over folklore.

A corner in [CORNERS.md](../../../prompts/CORNERS.md) is not absorbed
until it has one of these tests or a doctor check.

## CLI

`doctor --fail` is the gate. `explain` dumps Actions, Components, domains,
stamp, drivers.

## How an implementer is spawned

1. Confirm council strategy: [COUNCIL.md](../../../prompts/COUNCIL.md)
   (halt-or-patch, prompt-as-artifact).
2. If the skill’s law or author API changed, run
   [META_PRODUCT_LIBRARY.md](../../../prompts/META_PRODUCT_LIBRARY.md)
   and overwrite BUILD in place.
3. Hand the implementer [BUILD_PRODUCT_LIBRARY.md](../../../prompts/BUILD_PRODUCT_LIBRARY.md)
   plus the current [phase brief](../../../prompts/briefs/).
4. Follow [PLAN.md](../../../prompts/PLAN.md). Gate every phase.
5. On PATCH / HALT: test + fix + patch artifacts + append CORNERS.md.
   Re-run the same gate.

Do not hand an implementer any prompt that uses leftover public names.
Do not hand them ux-surface or uxkit source as a starting tree.
