# CEK model (how the new library uses it)

Law: [cek-framework CONCEPTS](https://github.com/bitplorer/cek-framework/blob/main/CONCEPTS.md)
· [CORE/06 Host and Peer](https://github.com/bitplorer/cek-framework/blob/main/CORE/06-host-peer.md)
· [CORE/11 Baseline and profile](https://github.com/bitplorer/cek-framework/blob/main/CORE/11-baseline-profile.md)
· [CORE/17 Extensibility](https://github.com/bitplorer/cek-framework/blob/main/CORE/17-extensibility.md)
· [KILL-CRITERIA](https://github.com/bitplorer/cek-framework/blob/main/KILL-CRITERIA.md)

Runtime: [cek-runtime CONCEPTS](https://github.com/bitplorer/cek-runtime/blob/main/CONCEPTS.md)
· [DRIVERS](https://github.com/bitplorer/cek-runtime/blob/main/DRIVERS.md)
· [profiles](https://github.com/bitplorer/cek-runtime/blob/main/06-profiles/README.md)

Catalog: [cek-python CATALOG_AUTHORITY_TARGET](https://github.com/bitplorer/cek-python/blob/main/docs/CATALOG_AUTHORITY_TARGET.md)

If a live file disagrees with this page, **the live file wins**.

---

## Roles

There are **exactly two** L1 kernels. There is no third.

```text
Host runtime  ⊃  Host kernel   mint · verify · once · project · lineage
Peer runtime  ⊃  Peer kernel   apply under profile · receipt
                 drivers       mutate kv / DOM / log  (not a kernel)
```

| Role | Does | Does not |
|------|------|----------|
| **Host** | Decide. Verify Cap. Dispatch. Record lineage. Project Ops. Return Result. | Rely on Peer to “confirm” Cap |
| **Peer** | Apply Ops in order under a profile. Optional receipt. | Mint Caps. Invent business truth |
| **driver** | Mutate one world (kv, DOM, log, or a product store) for one pair | Mint, verify, refuse Caps, speak law generation |

If Result is `authority_refusal` or `dispatch_error`, **no driver runs**.

This library is **L7**. It composes Actions that return Ops. It is not a
third kernel, not a second Channel, and not a rewrite of cek-surface.

---

## Layers (where this library sits)

```text
L7  application          THIS LIBRARY — App, Component, Action, domain registration
L6  policy               Channel hooks — cannot replace Cap
L5  domain drivers       Peer runtime registerDriver — product ships these
L4  profile              Peer apply ability (baseline, ui, production-v1)
L3  trace                Correlation only
L2  Activity · lineage   Host-owned
L1  Host / Peer kernels  Channel + optional cek-host / cek apply
L0  law                  cek-framework — do not rewrite
```

Flexibility lives in L4–L7. Security lives in L0–L2.

---

## Pair, domain, driver, profile, stamp

| Idea | Rule |
|------|------|
| **pair** | Identity is `(ns, name)`. `name` is one lowercase token. Dots live in `ns`. |
| **S** | Five pairs always understood: `kv.set`, `kv.delete`, `log.append`, `ui.dom.morph`, `ui.dom.restore`. |
| **domain stdlib** | JSON module `{ name, version, driver_hint, seed_pairs }`. Core: `baseline`, `ui`. Bundled example: `search` (`hits`, `clear`). |
| **agreement** | Host offers domains, Peer accepts, majors must match. Baseline is always included. |
| **stamp** | Union of agreed seed pairs for **this session**. Via negativa: absent = illegal. |
| **driver** | `registerDriver(ns, name, fn)` on the Peer runtime. Stamped extension with no driver → apply fails that Op. |
| **profile** | Apply ability (`baseline`, UI, `production-v1`). Never Cap power. Unknown Op policy: skip or fail-batch. |
| **Rust Peer kernel** | Applies **S only**. Extensions need a Peer **runtime** with a driver (JS `apply_s` / product drivers). |

```text
Host can project a stamped extension
Peer kernel (Rust) will skip it
Peer runtime (JS + registerDriver) will apply it
```

So a product feature that needs `search.hits` must:

1. Load the `search` stdlib.
2. `app.use("search")` so the stamp includes the pairs.
3. Ship or register a `search` driver on the Peer.
4. Doctor fails if stamp has pairs the Peer cannot apply.

Apps may add **their own** domains the same way (`orders.status`,
`billing.quote`, …). Structure (`cek_host.structure.validate_pair`):

- no `cek.` / `sys.` / `_` prefixes
- max two dots in `ns`
- `name` is one token
- reserved Baseline names `kv`, `log` cannot be reused as product domains

Two legality questions — do not mix them:

1. **Is it in S?** — core declaration.
2. **Is it in this session’s stamp?** — what Host may project and Peer may apply.

No stamp + open catalog mode → treat as S.
Stamp present → **only** the stamp.

---

## Two clocks (do not merge)

| Clock | Where | Allowed |
|-------|--------|---------|
| **Authority** | Host Action → `list[Op]` under a Cap | World changes, kv, morph, lineage |
| **Preview** | Peer runtime (coalesce, pending, optimistic paint, local filter) | Instant UI **only**. Never authority kv. Never entitlements. |

On the next Result: clear preview, then apply Ops.

Do **not** put preview calls inside the Ops list.
Do **not** name this “chrome” in the author API.

---

## Follow-up Actions

Multi-step UI (debounce → commit, timer → retry):

1. The Action that starts the wait calls `ctx.follow_up(event, action, args_from=…)`.
2. Adapter asks Channel / CEK to **mint** a continuation Cap (Host only).
3. Peer later emits the event and fills declared slots (`store.*`, `event.*`).
4. Host **verifies again** and runs the follow-up Action.

Bare `@app.on` handlers are fallback only. Prefer follow-up Actions so
every world change stays under a Cap.

---

## How this library reaches CEK

`ux-channel` already has the door. `cek-surface` **must not** depend on
ux-channel. This library depends on **ux-channel**, and optionally on CEK
*through* Channel — never the other way around.

```text
ChannelConfig.cek = off | adapt | require
```

| Mode | What happens |
|------|----------------|
| `off` (default) | Channel Caps + classic morph wire. Zero CEK imports. |
| `adapt` | CEK Host on the side. Channel Cap remains authority. |
| `require` | mint / verify / once / sealed-args go through `cek_host.Host`. Continuations via Channel’s CEK adapter. Classic morph Ops stay Channel wire. S pairs are what `Host.project_wire` accepts. |

**Application code still never imports CEK.** The adapter calls
`ux_channel.cek` only.

Channel uses cek-surface for **continuation compose** when `require` is
on. This library must not grow a second `CapService` or a second
`Surface.arm`.

---

## Composition language

Python is the composition language. The wire is only `Result.ops`.
No plan IR on the wire. No `eval`. No Peer-executable recipes.

```python
# Author — macros expand to legal pairs
return [
    update("cart.badge"),
    notify("Created", level="success"),
    go("/orders/1"),
]

# Author — explicit pair when extending a domain
return [
    Op("search", "hits", {"target": "results", "items": hits, "q": q}),
]
```

`Op(ns, name, payload)` is illegal to **emit** unless `(ns, name)` is in S
or the session stamp. Construction validates pair structure (`name` one
token). Submit / apply fail closed on an unstamped pair.

---

## Host pipeline this library must not skip

From CORE 06 / runtime CONCEPTS, fail closed, no side-effects before the gate:

1. Verify Cap (integrity, expiry, action bind, sealed args, optional subject / scopes).
2. Consume once / check idempotency. Required store down → refuse.
3. Dispatch the Action only after verify.
4. Record lineage when the Cap is revocable or the Activity is endable.
5. Project Ops to `profile ∩ stamp ∪ Baseline`.
6. Return Result.

This library’s adapter calls Channel (and Channel’s CEK door). It does
not reimplement the pipeline.
