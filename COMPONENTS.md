# COMPONENTS — ux-app author vocabulary

Markup and Tailwind tokens live in **ux-dom** (`ux_dom.ui`). This file is the
author surface for Host apps. `ux_app.ui` re-exports the kit when ux-dom is
installed. Ownership does not move.

```python
# preferred — ownership in ux-dom
from ux_dom.ui import Button, Card, Slider, Carousel, ToastHost, DatePicker, Chart
from ux_dom.ui.channel_bridge import stamp_region, live_button, public_form

# author DX alias (same objects)
from ux_app.ui import Button, ToastHost
```

Ownable copy (kernel untouched):

```bash
uxapp add ui Button
uxapp add ui Carousel --dest app/components/ui
# layers on `uxdom add ui` when ux-dom is installed
```

Every component is pure server HTML. Channel is optional. Local chrome
(tabs / dialog / carousel index) may use Alpine. Authority mutations are
`Action → list[Op]` under a Cap.

---

## Primitives

### Button

```python
Button("Save", type="submit", variant="default")
Button("Cancel", variant="outline", size="sm")
Button("Delete", variant="destructive", disabled=True)
```

Variants: `default` `secondary` `outline` `ghost` `destructive` `link`.
Sizes: `sm` `md` `lg` `icon`. `className=` always wins.

### Input / Textarea / Select / Checkbox / Switch / Slider / DatePicker

```python
Input(name="email", type="email", placeholder="you@work")
Input(name="q", invalid=True)
Textarea(name="bio")
Select(options=[("free", "Free"), ("pro", "Pro")], value="pro")
Checkbox(name="tos", id="tos")
Switch(checked=True, disabled=False)
Slider(name="volume", min=0, max=100, value=40, show_value=True)
DatePicker(name="due", value="2026-08-16")
DatePicker(name="due", invalid=True)   # empty + invalid states
```

DatePicker is native `type=date`. Litepicker is Phase 2 (declared
`Document.use` plugin) — this component never injects it.

### Card / Badge / Alert / Table

```python
Card(CardHeader(CardTitle("Cart")), CardContent(...), CardFooter(...))
Badge("live", variant="success")
Alert(AlertTitle("Heads up"), AlertDescription("Cap refused."), variant="warning")

Table(
    TableHeader(TableRow(TableHead("Sku", sorted="asc"), TableHead("Qty"))),
    TableBody(TableEmpty("No rows", col_span=2)),
)
```

---

## Composites

### Tabs / Dialog (Alpine local chrome)

```python
Tabs(items=[("a", "Account", div("…")), ("b", "Billing", div("…"))], default="a")

Dialog(
    trigger=Button("Confirm", variant="outline"),
    title="Pay now",
    body=div("Charge the card on file."),
    footer=live_button("Pay", action="Checkout.pay", target="Checkout:dialog"),
)
```

Declare the runtime so production doctor stays green:

```python
app.require_composite("dialog", "tabs")
app.declare_runtime("alpine")
```

### Carousel

```python
Carousel(slides=[div("One"), div("Two")], label="Highlights")
Carousel(slides=[])  # empty state
```

Index is Alpine-only. Server authority uses `stamp_region` + `live_button`.

### ToastHost

```python
ToastHost(items=[{"text": "Saved", "level": "success"}])
ToastHost(items=[])  # empty live region — still in the tree for morph
```

The list is **server authority**. Do not put business truth in `Alpine.store`.
`notify("Saved")` morphs `#notices` via S pairs. Richer notices use the
effects pack (below).

### Chart

```python
Chart(series=[4, 8, 6, 12], kind="sparkline", label="Revenue")
Chart(series=[2, 7, 4], kind="bar")
Chart(series=[])  # empty
```

SVG only. Chart.js is Phase 2 (declared plugin).

---

## Channel (optional)

```python
from ux_dom.ui.channel_bridge import (
    channel_available, stamp_region, live_button, public_form, to_fragment,
)

region = stamp_region(Dialog(body="…"), uid="Checkout:dialog")
live_button("Pay", action="Checkout.pay", target="Checkout:dialog")

# Progressive form: valid POST when Channel is absent
public_form(
    Input(name="sku"),
    action="cart.add",
    href="/actions/cart.add",
)
```

Every battery component renders with Channel absent. `live_button` degrades
to `data-channel-action` stubs.

After `ui.dom.morph`, stock `x_element.js` re-upgrades hosts. App code does
not implement re-upgrade.

---

## Continuation-first (R2)

Checkout / confirm is a Host-minted Cap chain. Peer never mints.

```python
from ux_app import App, action, Op

@action("checkout.start", caps=())
def start(ctx):
    ctx.follow_up("checkout.confirm", "checkout.pay", order_id=ctx.args["order_id"])
    return [Op.kv_set("checkout.phase", "confirm")]

@action("checkout.pay", caps=["checkout.write"])
def pay(ctx):
    return [Op.kv_set("paid", ctx.args["order_id"])]

app = App.bind()
app.submit("checkout.start", {"order_id": "o1"})
# emit without the Host Cap → ops [] and world unchanged
app.emit("checkout.confirm")
# emit with the minted Cap
cap = app.runtime.continuations["checkout.confirm"].cap
app.emit("checkout.confirm", cap=cap)
```

---

## Perception-native search (R3)

Typeahead uses `preview.filter` + `pending`. Commit is an Action.

```python
from ux_app import action, preview, Op
from ux_app.drivers import search_driver

@action("search.type", caps=())
def typeahead(ctx):
    q = ctx.args.get("q") or ""
    preview.filter("search:hits", q, "results")
    preview.pending("results", True)
    return [Op.kv_set("search.pending", q)]

@action("search.commit", caps=())
def commit(ctx):
    q = ctx.args["q"]
    return [Op("search", "hits", {"target": "results", "items": [q], "q": q})]

app.use("search", driver=search_driver)
```

Returning `PreviewCall` from an Action is `IllegalOp`. The next Result
clears preview, then applies Ops.

---

## Effects DomainPack (R1)

`notify()` stays S-only (`log.append` + `ui.dom.morph` of `#notices`).
Never emits undeclared `ui.toast`.

```python
from ux_app.effects import notice, clear_notices, effects_driver

app.use("effects", driver=effects_driver)

@action("orders.save", caps=())
def save(ctx):
    return notice("Saved", level="success")
```

Pairs: `ui.notice.push`, `ui.notice.clear`. Doctor fails them if stamped
and undriven.

---

## Doctor UI health (R7)

```python
app.require_composite("carousel", "dialog")
app.declare_runtime("alpine")
app.doctor(fail=True)   # production profile fails missing alpine
```

Stamped UI pairs without a driver already fail `domains.doctor_issues`.

---

## Inventory

| Component | Module | Runtime | Channel | Complete |
|-----------|--------|---------|---------|----------|
| Button | `ux_dom.ui.button` | none | stub via live_button | Y |
| Input | `ux_dom.ui.input` | none | — | Y |
| Select | `ux_dom.ui.select` | none | — | Y |
| Checkbox | `ux_dom.ui.checkbox` | none | — | Y |
| Switch | `ux_dom.ui.switch` | none | — | Y |
| Slider | `ux_dom.ui.slider` | none | — | Y |
| Table (+ Empty) | `ux_dom.ui.table` | none | stamp_region | Y |
| Tabs | `ux_dom.ui.tabs` | Alpine | — | Y |
| Dialog | `ux_dom.ui.dialog` | Alpine | stamp_region | Y |
| Carousel | `ux_dom.ui.carousel` | Alpine | stamp_region | Y |
| ToastHost | `ux_dom.ui.toast` | none (morph) | yes (`#notices`) | Y |
| DatePicker | `ux_dom.ui.datepicker` | native | — | Y |
| Chart | `ux_dom.ui.chart` | SVG | — | Y |
| public_form | `ux_dom.ui.channel_bridge` | none | yes / POST fallback | Y |
