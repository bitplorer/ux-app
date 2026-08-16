# Architecture

`ux-app` is an L7 author layer. It is not a third kernel.

```text
Author:  App · Component · Action · Event · State · Layout · Domain
              ↓  list[Op]   pairs must be in the session stamp
Adapter: only ux_channel / cek_* imports   (src/ux_app/adapter/**)
              ↓
Cores:   ux-dom      Document, Component tree, Tailwind, uxdom create-app
         ux-channel  Intent → Result → Ops, Caps, Peer
              └── ChannelConfig.cek = off | adapt | require
                    Host decide · domain stdlibs · drivers · profile
```

## Ownership

| This library | Not this library |
|--------------|------------------|
| App façade, Components, Actions, field State, Layouts | Document, routes, Tailwind (`ux-dom`) |
| Macros that expand to domain Ops (`update`, `notify`, `go`) | Cap mint / verify (`cek-host` / Channel) |
| Domain registration + driver wiring for the product | Peer kernel apply (`ux-peer-kernel` / `cek apply`) |
| Isolation so app code never imports Channel / CEK | A second wire protocol |

## Two runtimes, one law

There are exactly two L1 kernels: Host (decide) and Peer (apply).
`LocalRuntime` is an in-process Host + Peer used by `App.bind()` and by
`App.boot()` when the cores are not installed. It is **not** a third
kernel. It obeys the same law: verify before compose, refuse → `ops: []`,
pair identity, two clocks.

When `ux-dom` and `ux-channel` are installed, `adapter/boot.py` attaches
them. Application modules never import those packages. A mechanical
scan (`ux_app.isolation.scan_imports`) fails the doctor if they do.

Cold `import ux_app` does not import Channel, CEK, or wire codecs.

## Attach order

Peer kernel script, then preview script. Never reverse.

```html
<script src="ux-peer-kernel.js" data-role="peer-kernel"></script>
<script src="ux-peer-perception.js" data-role="preview"></script>
```

## Two clocks

| Clock | Where | Allowed |
|-------|--------|---------|
| Authority | Host Action → `list[Op]` under a Cap | World changes, kv, morph |
| Preview | Peer-local (`preview.pending` / `update` / `filter`) | Instant UI only. Never authority kv |

The next Result clears preview, then applies Ops. Preview is not an Op
and is illegal inside an Action's return.

## Caps

- `@action("orders.create", caps=["orders.write"])`. `caps=()` is the
  explicit public opt-out.
- Present Cap always verifies, even on a public Action.
- once-store down → refuse. Reuse of a once Cap → refuse.
- Follow-ups: Host mints the next Cap. Peer fills declared slots.
  Host verifies the sealed args again.

Profile (`ui`, `production`) negotiates apply ability, never Cap power.

## Pair identity

An Op is `(ns, name)` with `name` one token.

- `("ui.dom", "morph")` is legal
- `("ui", "dom.morph")` is illegal

S (always understood): `kv.set`, `kv.delete`, `log.append`,
`ui.dom.morph`, `ui.dom.restore`. Extensions join via `use` / `domain`,
must be on the session stamp, and need a Peer driver.

`cek=off` still maintains that pair set. Undeclared pairs never slip out.

## Isolation

Only `src/ux_app/adapter/**` may import `ux_channel` or `cek_*`.
CEK is reached through Channel's door (`adapter/cek.py`), never by
importing `cek_surface` from App code.

## Production profile

`App.bind(profile="production")` turns on a durable once-store flag
and receipts. Doctor fails that profile if either is missing.
