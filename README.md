# ux-app

Host-authored application layer on **ux-dom** + **ux-channel**.
Authors write Components and Actions that compose any CEK domain.
The Peer only applies Ops.

```python
from ux_app import App, Badge, Component


class CartBadge(Component):
    id = "cart.badge"
    count: int = 0

    def render(self):
        return Badge(self.count, on_click=self.add)

    def add(self, sku: str = ""):
        self.count += 1


app = App.boot(title="Cart")
app.add(CartBadge)
```

Click increments the badge. The Action returns nothing; a dirty session
field becomes `update("cart.badge")` → `ui.dom.morph`.

## Install

```bash
pip install -e .
# Optional live cores (not required for App.bind / tests):
# pip install "ux-dom @ git+https://github.com/bitplorer/ux-dom.git"
# pip install "ux-channel @ git+https://github.com/bitplorer/ux-channel.git#subdirectory=python"
# pip install "ux-app[cek]"
```

## What it is

- **App** — composition root. `boot()` stands up Document + Channel when
  they are installed, otherwise an in-process Host + Peer for tests.
- **Component** — a class with `id` + `render`. Dataclass fields default
  to session state.
- **Action** — named server function. Returns `list[Op]`. Caps required
  (`caps=()` is the public opt-out).
- **Domains** — `app.use("search")` or `app.domain(...)`. Same path for
  bundled and product packs. A stamped pair with no driver fails doctor.

## What it is not

- Not a second Channel, and not a rewrite of cek-surface.
- Not a closed toast / navigate catalog. Helpers expand to legal pairs.
- Not a website, React app, or SwiftUI port.
- Not a place that imports Channel from application code.

## Docs

- [START.md](START.md) — first morph in five minutes
- [ARCHITECTURE.md](ARCHITECTURE.md) — ownership vs the cores
- [DOMAINS.md](DOMAINS.md) — adding a pack and a driver
- [docs/AGENTS.md](docs/AGENTS.md) — maintainer map

Frozen CEK words (Cap, Host, Peer, Op, …) keep their meanings.
See [cek-framework CONCEPTS](https://github.com/bitplorer/cek-framework/blob/main/CONCEPTS.md).

## CLI

```bash
uxapp create-app shop          # layers on uxdom create-app when present
uxapp init
uxapp new component banner
uxapp new action orders.create
uxapp new domain orders
uxapp doctor --fail
uxapp explain
```

`--yes` is non-interactive. `--force` overwrites. They are not the same.

## Verify

```bash
make verify
```
