# Author API (day-1)

Developers should not mention Intent, CapService, HTMX, stamp, or profile.

## Boot

```python
from ux_app import App, Component, action, update, notify, go

app = App.boot(title="Acme")
# Document + Channel + domains baseline+ui + Peer apply + preview attach
# default Layout with one content region
# isolation on
```

`bind(document=..., channel=...)` exists for tests and hosts that already
have cores. Day-1 uses `boot()`.

Options (all have safe defaults):

| Option | Default | Notes |
|--------|---------|--------|
| `cek` | `"off"` | `"adapt"` / `"require"` only if `ux-channel[cek]` is installed |
| `domains` | `("baseline", "ui")` | Extra via `app.use(...)` |
| `profile` | `"ui"` | Peer apply set. Never Cap power |
| `client_state` | `("ui.theme", "ui.density")` | Allowlist |
| `secret` | from env in prod | Prod refuses memory once-store |

---

## Component + dataclass State

No required base class. A class with `id` and `render` is enough.
If the author subclasses ux-dom `Component` / `ReactiveComponent`, honor
it — do not wrap twice, do not fight `_ensure_init_chain`.

```python
class CartBadge(Component):
    id = "cart.badge"
    count: int = 0          # session (default)

    def render(self):
        return Badge(self.count, on_click=self.add)

    def add(self, sku: str = ""):
        self.count += 1     # None → update(self.id)
```

Field planes (markers, not magic strings in every assignment):

| Marker | Plane | Allowed |
|--------|-------|---------|
| (default) | session | UI working state. Not money. |
| `Client()` | client | Allowlisted keys only. Theme, density. |
| `Store()` | durable | Author’s DB / Channel db guards. |
| `Transient()` | render-only | Not persisted. |
| `Sealed()` | written only from signed Action args | Prices, qty, ids the Cap bound. |

Changing a session field in an Action dirties the Component → `update(id)`
is implicit if the Action returns `None`.

`on_click=` / `on_submit=` stamp the control in the adapter (mint Cap with
the args the handler will see). Authors never see Channel attribute names.

Validation of Action args and dataclass fields is pluggable (valio-style
field validators, or plain type checks). Integer sealed fields: no silent
coerce. Fail before the body.

---

## Actions

```python
@action("orders.create", caps=["orders.write"])
def create(ctx, sku: str, qty: int):
    # qty is sealed — integer, no silent coerce
    return [
        update("cart.badge"),
        notify("Created", level="success"),
        go(f"/orders/{sku}"),
    ]
```

- Namespaced name (`orders.create`).
- `caps=` required. `caps=()` is the explicit public opt-out.
- Return `list[Op]` (helpers included). Not a custom Result type.
- A Component method may return `None` → `update(self.id)`.
- Validate before the body. Field errors become morphs of error regions.
  Cap failure is `authority_refusal` with `ops: []` — never mixed with
  validation misses.

`ctx` has: `principal`, `args`, `follow_up(...)`, session / store access.
No Channel types.

---

## Events and follow-ups

```python
@action("search.type")
def search_type(ctx):
    q = ctx.args.get("q") or ""
    ctx.follow_up("input.idle:search", "search.commit", args_from={"q": "search.pending"})
    return [store_set("search.pending", q)]

@action("search.commit", caps=["search.read"])
def search_commit(ctx):
    hits = lookup(ctx.args["q"])
    return [Op("search", "hits", {"target": "results", "items": hits, "q": ctx.args["q"]})]
```

Input coalesce / pending / optimistic paint: **automatic** on bound
inputs (Peer preview). Authors do not call a preview API for the default
case.

Escape hatch (Peer-local, never lineage):

```python
preview.pending("results", True)
preview.update("hdr", {"text": "…"})
preview.filter("search:hits", q, "results")
```

Illegal inside an Action’s returned Ops list.

---

## Domains

```python
app.use("search")                    # bundled

app.domain(                          # product-specific
    name="orders",
    version="1.0.0",
    pairs=[("orders", "status")],
    driver=orders_status_driver,     # Peer apply; no mint
)
```

See [domains.md](domains.md) for the handshake, structure rules, and
doctor checks.

---

## Layout

One default Layout. Exactly one content region. Named side regions are
optional (`sidebar`, `notices`). Dispose on shutdown.

Do not invent `@shell` / `Frame` / `Main`.

---

## CLI

`create-app` **layers on** `uxdom create-app` (Document, routes, Tailwind).
Then adds App boot, default Layout, example Component.

Also: `init`, `new component|action|domain`, `doctor --fail`, `explain`
(registry dump: Actions, Components, domains, stamp, drivers).

Overwrite only with `--force`. `--yes` is not force.

---

## Isolation

Mechanical scan: only `ux_app/adapter/**` may import `ux_channel` or
`cek_*`. Fail closed in `App.boot` when strict.

Cold `import ux_app` must not import Channel, CEK, or wire codecs.

Root `__all__` stays small. Power APIs (stores, test harness, driver
helpers) live in subpackages, the way Channel keeps `host.stores` off root.
