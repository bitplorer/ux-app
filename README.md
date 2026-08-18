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

## Channel Result crossing

Author code stays on `update` / `notify` / `go`. When a Host must emit a
Channel `ops[]` (live Peer, or motion on the same Result), use the
adapter door — not a Host-local dict, not a fifth package:

```python
from ux_app.adapter import compose, lower_morph

ops = compose(
    lower_morph("#view", html),   # {op: morph, morph: idiomorph}
    scene.play(),                 # transition.* — no html on #view
)
```

Law on one Result: `morph(T)` XOR `scene.enter(T, html=…)`. Navigate
kinds are ordered last. `compose` / `lower_morph` speak wire *shape*
and do not import `ux_channel`. They are not on `ux_app.__all__`.

Play `transition.*` after Channel morph with `document.use(Motion(),
MotionChannel())` from **ux-motion**. Channel never learns those ops.

## Docs

- [START.md](START.md) — first morph in five minutes
- [ARCHITECTURE.md](ARCHITECTURE.md) — ownership vs the cores
- [DOMAINS.md](DOMAINS.md) — adding a pack and a driver
- [docs/AGENTS.md](docs/AGENTS.md) — maintainer map
- [docs/STACK_CLEANUP_COUNCIL.md](docs/STACK_CLEANUP_COUNCIL.md) — crossings

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
