# Corners log

Living immune system for the plan. The pre-mortem (C-pre-*) is
seeded from the live bitplorer stack **before** Phase 0. New corners
found in execution are appended, never rewritten away.

A corner is absorbed only when it has: **id · phase · test · artifact
sentence**. “Noted for later” is not absorption.

Scribe owns this file. See [COUNCIL.md](COUNCIL.md).

---

## Status

| Status | Meaning |
|--------|---------|
| `open` | Known risk. Brief must mention it. Test may not exist yet. |
| `absorbed` | Test (or doctor check) exists and the artifact warns. |
| `wont` | Council recorded why it is not a defect (cite live file). |

---

## Pre-mortem (known before code)

These are the weak edges the council expects. Phase briefs must
cite the ids that apply.

| Id | Phase | Corner | Prevention | Status |
|----|-------|--------|------------|--------|
| C-pre-01 | 0 | Public import named `surface` / `uxkit` / `cek_surface` | Freeze `ux_app`. Scan `__all__` | absorbed · `tests/test_public_api.py` |
| C-pre-02 | 0 | Banned leftover names leak into types | vocabulary.md banned table + `__all__` test | absorbed · `tests/test_public_api.py` |
| C-pre-03 | 1 | Cold `import ux_app` loads Channel / CEK / codecs | Isolation scan from day one | absorbed · `tests/test_isolation.py` |
| C-pre-04 | 1 | App modules import `ux_channel` outside `adapter/` | Doctor fail-closed at boot when strict | absorbed · `tests/test_isolation.py` · `ux_app.doctor` |
| C-pre-05 | 1 | Peer kernel attached after preview (wrong order) | Kernel **then** preview attach | absorbed · `tests/test_app.py::test_boot_empty_page_has_scripts_in_order` |
| C-pre-06 | 1 | `cek=off` has no pair set, so undeclared pairs slip out | Adapter maintains a session pair set in every mode | absorbed · `tests/test_domains.py::test_cek_off_still_has_pair_set_and_refuses_undeclared` |
| C-pre-07 | 1 | Competing `create-app` that fights `uxdom` | CLI layers on `uxdom create-app` only | absorbed · `tests/test_cli.py` · `cli/main.py` |
| C-pre-08 | 2 | Double-wrap of ux-dom `ReactiveComponent` / broken `_ensure_init_chain` | Honor subclass; do not wrap twice | absorbed · `tests/test_component.py` |
| C-pre-09 | 2 | Money / qty / roles on the client plane | Doctor + type gate on money-shaped names | absorbed · `tests/test_state.py::test_money_shaped_client_fails_type_gate` |
| C-pre-10 | 2 | Silent string→int coerce of sealed qty (`"1"`) | Reject. No coerce | absorbed · `tests/test_state.py` · `tests/test_actions.py` |
| C-pre-11 | 2 | Control minted without the args the handler will see | Adapter mints with those args | absorbed · `adapter/runtime.py::mint_control` · golden cart `data-args` |
| C-pre-12 | 3 | Second result type (`reply`, `ActionResult`, `Effect`) | Actions return `list[Op]` only | absorbed · `tests/test_public_api.py` · `as_ops` |
| C-pre-13 | 3 | Cap refuse still emits morphs | Verify before compose. `ops: []` | absorbed · `tests/test_actions.py::test_cap_refuse_empty_ops_world_unchanged` |
| C-pre-14 | 3 | Present bogus Cap on a public Action skips verify | Present Cap always verifies | absorbed · `tests/test_actions.py::test_present_bogus_cap_on_public_still_verifies` |
| C-pre-15 | 3 | once-store down still runs the Action | Refuse | absorbed · `tests/test_actions.py::test_once_store_down_refuses` |
| C-pre-16 | 3 | `notify` / `go` emit undeclared `ui.toast` / `nav.push` | Macros expand to S or a stamped domain | absorbed · `tests/test_ops.py::test_notify_and_go_expand_to_s_only` |
| C-pre-17 | 3 | Unescaped morph / notify text | HTML-escape display text | absorbed · `tests/test_ops.py::test_notify_escapes_html` |
| C-pre-18 | 4 | Split-alias pair treated as legal (`ui` + `dom.morph`) | Pair identity. `name` is one token | absorbed · `tests/test_ops.py::test_pair_identity_split_alias_illegal` |
| C-pre-19 | 4 | `use("search")` without a driver, doctor green | Doctor fails. Rust kernel applies S only | absorbed · `tests/test_domains.py::test_use_search_without_driver_fails_doctor` |
| C-pre-20 | 4 | Overwriting core stdlib `baseline` / `ui` | Illegal | absorbed · `tests/test_domains.py::test_cannot_overwrite_core_stdlib` |
| C-pre-21 | 4 | Product domain with empty `seed_pairs` | Illegal at register | absorbed · `tests/test_domains.py::test_empty_seed_pairs_illegal` |
| C-pre-22 | 4 | `ns` with `cek.` / `sys.` / `_` prefix or too many dots | `validate_pair` rules | absorbed · `tests/test_ops.py` |
| C-pre-23 | 4 | Catalog `open` vs `strict` mixed up with stamp | No stamp + open → S; stamp present → stamp only | absorbed · `tests/test_domains.py` · Peer `unknown="strict"` |
| C-pre-24 | 5 | Preview written into the returned Ops list | Illegal. Preview is Peer-local | absorbed · `tests/test_preview.py::test_preview_not_an_op_return` |
| C-pre-25 | 5 | Preview writes authority kv | Adversary test. Must not | absorbed · `tests/test_preview.py::test_preview_does_not_write_authority_kv` |
| C-pre-26 | 5 | Peer fires a follow-up without the Host Cap | Host mints; Host verifies again | absorbed · `tests/test_events.py::test_follow_up_requires_host_cap` |
| C-pre-27 | 5 | Preview still painted after the next Result | Clear preview, then apply | absorbed · `tests/test_preview.py::test_preview_cleared_after_result` |
| C-pre-28 | 5 | Bare `@app.on` used for world-changing next steps | Prefer `follow_up` | absorbed · no `@app.on` shipped · `events.py` |
| C-pre-29 | 6 | `--yes` treated as `--force` | Distinct flags | absorbed · `tests/test_cli.py::test_yes_is_not_force` |
| C-pre-30 | 6 | Second scaffold tree next to `uxdom` | Layer only | absorbed · `tests/test_cli.py::test_create_app_layers_and_respects_force` |
| C-pre-31 | 7 | Sync submit of an async Action nests a loop | Sync refuses; `async_submit` runs it | absorbed · `tests/test_actions.py::test_async_action_sync_refuses_async_runs` |
| C-pre-32 | 7 | production profile without durable once-store / receipts | Doctor fails that profile | absorbed · `tests/test_app.py::test_production_profile_doctor_requires_durable_and_receipts` |
| C-pre-33 | * | cek-surface still exposes leftover verbs internally | Adapter must not re-export. Author API is `preview` / `follow_up` | absorbed · `tests/test_public_api.py` |
| C-pre-34 | * | Channel classic IR still has toast / navigate | Those are Channel wire, not this library’s catalog | absorbed · `tests/test_ops.py::test_notify_and_go_expand_to_s_only` |
| C-pre-35 | * | Live file disagrees with this skill | Live file wins. Scribe patches | wont · procedure (COUNCIL §2). Not a code defect. |

---

## Found in execution

| Id | Phase | Corner | Prevention | Status |
|----|-------|--------|------------|--------|
| C-001 | 3 | `Op("search","hits",…)` cannot be written if the constructor requires a stamp the author does not hold | Construction validates **structure**. Stamp is enforced at **emit** (`check_stamp` / `Op.stamped`). Author-api examples stay legal. | absorbed · `ops.py` · `tests/test_domains.py` · `cek-model.md` patched |
| C-002 | 6 | Workspace root `AGENTS.md` is the sandbox agent file; overwriting it would erase the agent contract | Library maintainer map lives at `docs/AGENTS.md`. README links it. Phase 6 brief cites this. | absorbed · `docs/AGENTS.md` · `briefs/phase-6.md` |
| C-003 | 3 | Cap tokens encoded as `id.exp.action.digest.once.sig` break on dotted Action names (`cart.badge.add`) → `cap malformed` | Tokens are `base64url(json).sig`. Adversary: golden cart click. | absorbed · `adapter/caps.py` · `tests/test_golden_cart.py` |
| C-004 | 2 | `from __future__ import annotations` stores `"int"` not `int`, so sealed no-coerce never fired | Compare annotation to both `int` and `"int"`. | absorbed · `component.py` · `action.py` · `tests/test_state.py` |

Every pre-mortem row is `absorbed` or an explicit `wont`. Phase 7 gate
may Advance.
