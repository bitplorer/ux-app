# Domains — any pack, same path

cek-surface’s real freedom is not a UI kit. It is this: **any versioned
domain can join a session**, Host and Peer agree, Host stamps the closed
pair set, and a Peer **driver** applies each pair. This library must
expose that path as the product, not hide it behind a closed Effect list.

Live sources (win on conflict):

- [cek-python domain_stdlib.py](https://github.com/bitplorer/cek-python/blob/main/cek-surface/src/cek_surface/domain_stdlib.py)
- [cek-python CATALOG_AUTHORITY_TARGET.md](https://github.com/bitplorer/cek-python/blob/main/docs/CATALOG_AUTHORITY_TARGET.md)
- [cek-host structure.py](https://github.com/bitplorer/cek-python/blob/main/cek-host/src/cek_host/structure.py)
- [cek-runtime domain.rs](https://github.com/bitplorer/cek-runtime/blob/main/crates/cek-contract/src/domain.rs)
- [cek-runtime DRIVERS.md](https://github.com/bitplorer/cek-runtime/blob/main/DRIVERS.md)
- [search.stdlib.json](https://github.com/bitplorer/cek-python/blob/main/cek-surface/stdlibs/search.stdlib.json)

---

## One sentence

A **domain** is a versioned pack of pairs. A **driver** is the Peer-side
function that applies one pair. A **profile** says which packs this Peer
can apply. A **stamp** is the closed pair set for **this session**.

Authors never mint Caps. Drivers never mint Caps. Profiles never grant
Cap power.

---

## Handshake

```text
1. Load   stdlib JSON or app.domain(...)
2. Offer  Host offers names + versions
3. Accept Peer accepts a subset (majors must match)
4. Stamp  Host sends { type: stamp, pairs: [{ns, name}, ...] }
5. Ack    Peer replies stamp_ack
6. Drive  every stamped pair is S or has registerDriver(ns, name, fn)
```

There is no on-the-wire `agree` message. Version intersection happens in
the Host runtime (via Channel’s CEK adapter when `cek != off`; via the
library adapter’s domain table when `cek = off`).

Baseline is **always** included.

Default boot agrees `{baseline, ui}` → stamp = **S**.

---

## Structure (fail closed at register)

From `cek_host.structure.validate_pair`:

| Rule | Example |
|------|---------|
| `ns` tokens: lowercase ASCII letters, digits, dots | `orders`, `ui.dom` |
| max two dots in `ns` | `billing.quote` ok; `a.b.c.d` illegal |
| no `cek.` / `sys.` / `_` prefixes | `cek.secret` illegal |
| `name` is one token, no dots | `status` ok; `dom.morph` illegal |
| reserved Baseline names not reused as product domains | cannot register a new `kv` / `log` domain |

Pair identity: `("ui.dom", "morph")` legal; `("ui", "dom.morph")` illegal
even though they concatenate to the same string.

---

## Bundled vs product domains

| Kind | How authors enable it | Who ships the driver |
|------|------------------------|----------------------|
| **Core** `baseline`, `ui` | Automatic on `App.boot()` | This library, via Channel / Peer attach |
| **Bundled example** `search` | `app.use("search")` | This library ships a small driver |
| **Product** `orders`, `billing`, … | `app.domain(name, version, pairs, driver=...)` | The app (or a plugin package) |

Same handshake. Same stamp. Same doctor.

```python
app.use("search")                      # bundled stdlib

app.domain(
    name="orders",
    version="1.0.0",
    pairs=[("orders", "status")],
    driver=orders_status_driver,       # Peer apply; no mint
)
```

A domain with no `seed_pairs` is illegal.
Overwriting a **core** stdlib (`baseline`, `ui`) is illegal.

---

## What each apply path will actually apply

| Path | Applies |
|------|---------|
| Channel Peer + JS `apply_s` / perception attach | Stamp ∩ (built-in S drivers ∪ `registerDriver`) |
| Rust `cek-peer-kernel` / `cek apply` | **S only**. Extensions are skipped. |
| Memory / test carrier | Echoes Ops. Not a kernel. |

Doctor rule: if the session stamp contains a pair that is not S and has
no registered driver, **fail**. Do not ship a library that projects
`search.hits` onto a Peer that will silently skip it.

When `cek = off`, the adapter still maintains a session pair set and
refuses to emit undeclared pairs. Classic Channel morph Ops are the
lowering of `ui.dom.morph` onto Channel’s existing wire — they are not a
second catalog.

---

## Drivers (the world)

A driver sits **outside** the Peer kernel.

```text
Host kernel  →  Result{Ops}
Peer kernel  →  asks a driver to apply each Op
driver       →  mutates kv / DOM / log / product store
```

A driver **must never**:

- mint or verify a Cap
- turn a refusal Result into world changes
- widen scopes, attach signatures, or speak law generation
- treat `trace` as permission
- invent a missing DOM node (missing target → that Op fails)

Adding a driver:

1. Declare the pair in a stdlib or `app.domain(...)`.
2. Implement apply only — no Host verify.
3. Register on the Peer runtime.
4. Document Baseline lowering (equivalent classic Ops or safe no-op)
   so a thin profile still works.

---

## Profiles

| Profile | Expectation |
|---------|-------------|
| **baseline** | Classic Ops; receipts optional |
| **ui** | Baseline + `ui.dom.morph` / `restore` |
| **production-v1** | Idempotency + receipts + fail-closed once-store |

`App.boot(profile="ui")` is the day-1 default. Profile negotiates **apply
ability**, not Cap power. Unknown Op policy is `strict` for this library
(fail the batch) unless the author opts into `tolerant` for a named pack.

---

## Macros vs domains

| Author writes | Expands to | Requires |
|---------------|------------|----------|
| `update("cart.badge")` | `("ui.dom", "morph", {target, patch})` | `ui` (default) |
| `notify("Saved")` | `("notice", "show", …)` if `notice` is stamped + driven; else `log.append` + morph of a notices region | never invents `ui.toast` |
| `go("/orders/1")` | `kv.set("ui:nav", …)` + optional morph | never invents `nav.push` |
| `Op("search", "hits", …)` | as written | `search` on the stamp + driver |
| `Op("orders", "status", …)` | as written | product domain on the stamp + driver |

If you want a rich notice or navigation pack, **declare it as a domain**
and ship a driver. Do not grow a closed `KNOWN_KINDS` list.

---

## Doctor checks (domain)

- every stamped pair is S or has a driver
- no pair with a dotted `name`
- no forbidden `ns` prefix
- majors of Host offer and Peer accept match
- core stdlibs were not overwritten
- production profile: durable once-store, receipts on
