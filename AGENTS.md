# Maintainer map

This package is **ux-app** (import `ux_app`, CLI `uxapp`).

## Hand-written

| Path | Job |
|------|-----|
| `src/ux_app/*.py` | Author API. Must not import Channel / CEK |
| `src/ux_app/adapter/*.py` | Only place `ux_channel` / `cek_*` may be imported |
| `src/ux_app/stdlibs/*.json` | Bundled domain packs |
| `src/ux_app/cli/main.py` | `uxapp` — layers on `uxdom`, never fights it |
| `tests/` | Contract tests. A corner is not absorbed without one |
| `prompts/` | Council, plan, corners, phase briefs |
| `.grok/skills/product-library/` | Playbook. Live bitplorer files win on conflict |

## Generated

| Path | Generator |
|------|-----------|
| `shop/app.py` from `uxapp create-app` | CLI template (`cli/main.py` `CART_APP`) |
| `uxapp new component\|action\|domain` | CLI stubs |

Do not check generated app trees into this repo. `examples/cart.py` is
the golden hand-written cart.

## Do not

- Start from ux-surface or uxkit source
- Export leftover names (see vocabulary.md banned table)
- Import Channel outside `adapter/`
- Treat profile as Cap power
- Scaffold a website

## Verify

```bash
make verify
```

Gates: unit tests, isolation scan, public `__all__` scan, `uxapp doctor --fail`.
