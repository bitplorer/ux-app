# Inspiration — take ideas, not APIs

Every bitplorer library teaches something. This library is **new**.
Copy the job, not the public names.

---

## What to take

| Source | Take | Leave |
|--------|------|-------|
| **cek-framework** | Frozen words. Host decides / Peer applies. Baseline. Kill criteria. Naming law (intention, not fashion). One concept, one name. | Rewriting law into product docs as a second glossary |
| **cek-runtime** | Runtime ⊃ kernel. Drivers sit outside the Peer kernel. Profiles negotiate apply ability. Pair identity in `domain.rs`. Receipts guide reverse. production-v1 = idempotency + receipts + fail-closed once-store | Linking mint into the Peer. A third kernel. `extensions/` layer |
| **cek-host** | mint / verify / once / sealed-args. Refuse → empty Ops. BoundAsk before dispatch. `structure.validate_pair`. doctor / explain | Growing a second CapService in this library |
| **cek-surface** | Domain stdlibs. Agreement + stamp. `Op(ns, name, payload)`. Continuations (Host-minted). Two clocks. Python is the composition language. Macros that expand to S | `chrome_*`, `arm`, `plan()` as IR, `signal_set` as a domain, Carrier as a product concept, a second `Surface` type |
| **ux-channel** | Intent → Result → Ops. Caps over args. Regions. `state()` planes. `ChannelConfig.cek`. Cold import. Small root `__all__`. doctor / create-app / explain. Peer kernel **then** perception attach. Conformance vectors win | Reimplementing Channel. Classic toast / navigate as a closed catalog this library owns. Importing Channel from app code |
| **ux-dom** | `Document`, `Component`, `ReactiveComponent` (fail-closed re-render, per-root lock, dataclass init-chain). Tailwind. `uxdom create-app`. DirectoryRouting | A parallel asset registry. Fighting `_ensure_init_chain`. A second CSS framework |
| **valio** | Dataclass-native field validation. Pre / post validators. Fail closed when debug / strict. No silent coerce | Inventing a competing validation DSL. Shipping valio as a required dep unless the author opts in |
| **uidom** | Server-rendered HTML, Tailwind, component composition | Alpine / HTMX as the product story (ux-dom already owns the document) |
| **uid-channel** | Historical: Intent → Action → Result(ops) | Anything it was replaced by in ux-channel |

---

## What not to take (sibling product libraries)

| Source | Idea worth keeping | Mistake to leave behind |
|--------|--------------------|-------------------------|
| **ux-surface** | Isolation (only adapter imports Channel). Caps on named operations. Public ids for live targets. Fail-closed registry | Closed `Effect` / `KNOWN_KINDS`. `reply(*effects)`. `Partial`. `@shell` / `Frame` / `Main`. In-memory `state`. `Theme` as a string name. Competing `create-app`. Commented-out Acme. Starting from `src/surface/**` and “finishing the stub” |
| **uxkit** | Drop-in / copied UI primitives. Dataclass / descriptor State. Security defaults (CSP, CSRF) | Vendoring `ux_dom` and `ux_channel` inside the package. SwiftUI cargo-cult (`VStack` as the product). `ActionResult(ok, flash, redirect)`. Duplicate Channel / Store. “Enterprise” checklist without Caps or a real wire |

---

## Design stance this library inherits

From Channel **longevity / cold import**: root is the application surface
only. Power APIs stay in packages.

From CEK **extensibility**: extend upward and outward; do not tunnel
through the law. New domain Ops are L5. They must be projectable or
ignorable for Baseline Peers.

From ux-dom **automation**: generate boring project files with the CLI;
hand-code only contracts. Layer on `uxdom create-app` — do not fight it.

From valio **fields**: state and Action args are dataclass fields with
validators, not a parallel form language.

---

## Honest non-goals

- Not a second Channel
- Not a second cek-surface
- Not a SwiftUI port
- Not a React / TypeScript author API
- Not a website, gallery, or marketing page
- Not a closed toast / navigate / focus catalog
- Not a rewrite of `ux-peer-kernel.js` or `ux-peer-perception.js`
