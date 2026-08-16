# Phase 1 SHIP proofs — ux-app 0.2.0 + ux-dom UI battery

Scribe paste. Agents ran every command. User was not asked to run proofs.

## 1. HEAD SHAs

| Repo | Start | End (this tree) |
|------|-------|-----------------|
| ux-app | `4b559dc538436ab6104622fdad3cc3983ae8b111` | working tree 0.2.0 (battery) |
| ux-dom | `debb24e8abcbbbae8306329f61eb7086964631cd` | working tree + UI battery |

## 2. isolation.scan_imports

```
isolation clean
```

No `ux_channel` / `cek_*` imports outside `src/ux_app/adapter/**`.

## 3. pytest / make verify

```
82 passed
isolation clean
public clean
doctor: ok
```

`notify()` still expands only to S pairs (`test_notify_still_s_only`, `test_notify_and_go_expand_to_s_only`).

## 4. doctor --fail

```
doctor: ok
```

Package profile. App-level undriven pairs remain soft at boot (`stamped pair ` prefix). Production profile fails undeclared Alpine (`test_production_fails_undeclared_alpine`).

## 5. Inventory

| Component | Module | Runtime | Channel | Complete |
|-----------|--------|---------|---------|----------|
| Button | ux_dom.ui.button | none | live_button stub | Y |
| Input | ux_dom.ui.input | none | — | Y |
| Select | ux_dom.ui.select | none | — | Y |
| Checkbox | ux_dom.ui.checkbox | none | — | Y |
| Switch | ux_dom.ui.switch | none | — | Y |
| Slider | ux_dom.ui.slider | none | — | Y |
| Table + Empty | ux_dom.ui.table | none | stamp_region | Y |
| Tabs | ux_dom.ui.tabs | Alpine | — | Y |
| Dialog | ux_dom.ui.dialog | Alpine | stamp_region | Y |
| Carousel | ux_dom.ui.carousel | Alpine | stamp_region | Y |
| ToastHost | ux_dom.ui.toast | none (morph) | #notices | Y |
| DatePicker | ux_dom.ui.datepicker | native | — | Y |
| Chart | ux_dom.ui.chart | SVG | — | Y |
| public_form | ux_dom.ui.channel_bridge | none | POST + stub | Y |

## 6. Golden morph path

`tests/test_transactional.py::test_multi_region_ops_in_one_action` — badge + rail + notices in one Action. Dialog/Carousel stamp + live_button locked in `tests/02_document_plugins/test_ui_battery.py`.

## 7. follow_up Cap + preview-then-commit

- `tests/test_transactional.py::test_checkout_follow_up_without_cap_unchanged`
- `tests/test_events.py::test_follow_up_requires_host_cap`
- `tests/test_perception_commit.py::test_preview_then_commit`
- PreviewCall return → dispatch_error (`test_preview_returned_from_action_is_illegal`)

## 8. Morph × XElement / Alpine coexistence

`test_morph_xelement_contract_markup` — stamped Carousel keeps `data-channel-id` + `x-data`. App code does not implement re-upgrade. Stock `x_element.js` scan remains the only CE runtime.

## 9. Antifragility batteries

| Battery | Result | Evidence |
|---------|--------|----------|
| C3.1 Isolation | PASS | `scan_imports() == []` |
| C3.2 Cap refuse | PASS | `test_cap_refuse_empty_ops_world_unchanged` |
| C3.3 Stamp | PASS | `test_effects_refuse_undeclared_leaves_world` |
| C3.4 Preview | PASS | `test_preview_not_an_op_return` / perception tests |
| C3.5 Optional-Channel | PASS | `test_every_battery_renders_without_channel` |
| C3.6 Morph × XElement | PASS | coexistence markup test (browser re-upgrade is stock JS) |
| C3.7 Quality ≥ HEAD | PASS | 82 tests, doctor, isolation, public |
| C3.8 Completeness | PASS | empty/disabled/invalid on Slider, Carousel, Toast, DatePicker, Chart, Table |

## 10. Critic scores (loop 1)

| Plane | Score | Notes |
|-------|-------|-------|
| W0 cartography | 5 | HEADs matched 4b559dc / debb24e |
| W1 primitives | 4 | Slider + disabled/invalid; no second token system |
| W2 composites | 4 | Empty states; Toast is morph-authority not Alpine.store |
| W3 radical | 5 | effects pack, follow_up, preview, doctor UI health, public_form |
| NORTH_STAR | 5 | thin Host, no author JS, no second CE runtime |
| Isolation / Cap | 5 | notify() unchanged S-only |
| Completeness | 4 | Chart.js / Litepicker deferred Phase 2 (signed) |

Residual disagreement:
- Chart.js in package-static vs SVG first → lean SVG (Phase 1). Chart.js is a declared plugin later.
- effects as stdlib vs folding into ui.notice S pairs → lean stdlib. `notify()` must stay S-only.

## 11. Council seats

| Seat | Gate |
|------|------|
| LAW | PASS — no Cap soften, no undeclared pair emit |
| DOMAIN | PASS — effects pack + driver; undriven fails doctor |
| DOCUMENT | PASS — kit extended in ux-dom.ui; ux_app.ui is a re-export |
| CHANNEL | PASS — optional; public_form POST fallback |
| AUTHOR | PASS — COMPONENTS.md + copy-paste examples |
| ADVERSARY | PASS — refuse paths + empty states; not demo-only |
| CRITIC | PASS — all planes ≥ 4 |
| LEADER | PASS — merge in this tree |

## Self-inversion

1. Still thin Host + minimal JS + CEK law? **Yes.** Battery is ux-dom HTML + DomainPack. No second kernel, no client authority store.
2. Council rubber-stamp? **No.** notify() was not grown; Chart.js and Litepicker were refused for Phase 1.
3. Production-usable / stable / complete? **Yes** for listed surfaces. Residual: datepicker a11y is native; Chart is SVG-only; toast authority is the Host list.

Kill triggers not tripped.
