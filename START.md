# Start — first morph in five minutes

## 1. Install

```bash
pip install -e ".[dev]"
```

You do not need ux-dom or ux-channel on the path to run the cart.
`App.boot()` uses an in-process Host + Peer when those packages are
missing. Install them later to attach a live Document and Channel.

## 2. One file

Save as `app.py` (or run `examples/cart.py`):

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

print(app.html("cart.badge"))
app.click("cart.badge")
print(app.world.ui["cart.badge"])
```

## 3. What you should see

The first print is a button labelled `0` with `data-action` and
`data-cap` on the control. After `click`, the morph target is `1`.

That is the whole loop: render → mint Cap with the args the handler
will see → verify → Action → `list[Op]` → Peer apply.

## 4. Add a domain

```python
from ux_app.drivers import search_driver

app.use("search", driver=search_driver)
```

Without the driver, `app.doctor()` fails. With it, an Action may return
`Op("search", "hits", {"target": "results", "items": [...], "q": q})`.

## 5. Next

- Field planes: `Client()`, `Store()`, `Transient()`, `Sealed()`
- Follow-ups: `ctx.follow_up("input.idle:search", "search.commit", …)`
- Product pack: `app.domain("orders", "1.0.0", [("orders", "status")], driver=…)`

Read [DOMAINS.md](DOMAINS.md) before inventing a pair.
Run `uxapp doctor --fail` before you ship.
