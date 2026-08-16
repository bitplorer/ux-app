# Domains

A **domain** is a versioned pack of pairs. A **driver** is the Peer-side
function that applies one pair. A **profile** says which packs this Peer
can apply. A **stamp** is the closed pair set for this session.

Authors never mint Caps. Drivers never mint Caps. Profiles never grant
Cap power.

## Handshake

```text
1. Load   stdlib JSON or app.domain(...)
2. Offer  Host offers names + versions
3. Accept Peer accepts a subset (majors must match)
4. Stamp  Host closes the pair set for this session
5. Drive  every stamped pair is S or has a driver
```

Baseline is always included. Default boot agrees `{baseline, ui}` →
stamp = **S**.

When `cek != off`, agreement goes through Channel's CEK adapter.
When `cek = off`, the library adapter still maintains the pair set.

## Structure (fail closed)

| Rule | Example |
|------|---------|
| `ns` tokens: lowercase ASCII letters, digits, dots | `orders`, `ui.dom` |
| max two dots in `ns` | `billing.quote` ok; `a.b.c.d` illegal |
| no `cek.` / `sys.` / `_` prefixes | `cek.secret` illegal |
| `name` is one token, no dots | `status` ok; `dom.morph` illegal |
| reserved Baseline names not reused as product domains | cannot overwrite `kv` / `log` |

Pair identity: `("ui.dom", "morph")` legal; `("ui", "dom.morph")` illegal
even though they concatenate to the same string.

## Bundled vs product

```python
app.use("search")                       # stamps pairs; doctor red until driven
app.use("search", driver=search_driver) # stamps + registers the bundled driver

app.domain(
    name="orders",
    version="1.0.0",
    pairs=[("orders", "status")],
    driver=orders_status_driver,        # Peer apply; no mint
)
```

A domain with no seed pairs is illegal.
Overwriting a core stdlib (`baseline`, `ui`) is illegal.

The Rust Peer kernel applies **S only**. Extensions need a runtime
driver. Doctor fails a stamped pair with no driver.

## Macros vs domains

| Author writes | Expands to | Requires |
|---------------|------------|----------|
| `update("cart.badge")` | `("ui.dom", "morph", {target, patch})` | `ui` (default) |
| `notify("Saved")` | `log.append` + morph of `notices` | never invents `ui.toast` |
| `go("/orders/1")` | `kv.set("ui:nav", …)` + morph | never invents `nav.push` |
| `Op("search", "hits", …)` | as written | `search` on the stamp + driver |
| `Op("orders", "status", …)` | as written | product domain on the stamp + driver |

If you want a rich notice or navigation pack, declare it as a domain
and ship a driver.

## Profiles

| Profile | Expectation |
|---------|-------------|
| `baseline` | Classic Ops |
| `ui` (default) | Baseline + `ui.dom.morph` / `restore` |
| `production` / `production-v1` | Idempotency + receipts + fail-closed once-store |

Unknown Op policy is `strict` (fail the batch).
