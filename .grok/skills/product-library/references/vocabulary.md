# Vocabulary

Two layers. Do not mix them.

Names answer **intention**, not mechanism fashion. One concept, one name.
Method (from CEK META 04): write the job in one sentence → score candidates
for intention clarity, developer familiarity, collision risk, decades
stability → freeze. Prefer a precise word over a popular vague one when
the job is accountability.

---

## Frozen (CEK / Channel — never rename)

Use only when speaking about the wire, authority, or apply path.

| Word | Meaning | Not |
|------|---------|-----|
| **Cap** | Permission ticket for one Action + sealed args | Session cookie, “logged in” |
| **Intent** | `{ action, args, cap }` | A React event |
| **Host** | Decides: verify, project Ops, lineage | The browser |
| **Peer** | Applies Ops under a profile | A place to put business logic |
| **Op** | `{ ns, name, payload }` — pair identity | A JS callback |
| **Result** | Host answer: `ok` / `authority_refusal` / `dispatch_error` | HTTP status alone |
| **Baseline** | Permanent pairs: `kv.set`, `kv.delete`, `log.append` | “Whatever we shipped this week” |
| **S** | Baseline ∪ UI seed (`ui.dom.morph`, `ui.dom.restore`) | An open catalog of toast / navigate |
| **pair** | `(ns, name)` — `name` is one token, no dots | Concatenated FQ as identity |
| **domain** | Versioned pack of pairs (e.g. `search`, `ui`) | A CSS namespace |
| **driver** | Peer-side apply for a pair. Outside the kernel. No mint. | A kernel, a policy engine |
| **profile** | What this Peer can apply (Baseline, UI, production-v1) | Cap authority |
| **stamp** | Closed pair set for **this session** after Host↔Peer agreement | A global allow-all |
| **receipt** | Landed vs failed Ops. Guides reverse. Not a Cap | Permission |
| **trace** | Correlation only | Permission |
| **Activity** | Bounded job with a lifetime (can end → reverse) | A thread, a fiber |
| **lineage** | Cause trail under Cap / Activity | History, audit log as authority |

Do not invent a second official language for these (CEK K10).

---

## Author-facing (what developers type)

Standard product words. Map onto the frozen layer in the adapter.
Day-1 authors should not need to say Intent, Cap, stamp, or profile.

| Developer says | Job (one sentence) | Maps to |
|----------------|--------------------|---------|
| **App** | Composition root I boot once | Host runtime + Document bind |
| **Component** | Drop-in UI unit with `id` + `render` | ux-dom Component; live target for `ui.dom.morph` |
| **Layout** | Named page frame, one content region | Document slots — not a second shell DSL |
| **Region** | Stable live target id | Channel region / morph target |
| **Action** | Named server function | Channel / CEK action; requires Caps |
| **Event** | User or system occurrence | Peer event → Host follow-up or local preview |
| **State** | Dataclass fields on a Component | session (default) / client (allowlist) / store |
| **update(id)** | Re-render that Component | `("ui.dom", "morph", {target, patch})` |
| **notify(text)** | Transient user message | Domain `notice` if stamped + driven, else `log.append` + morph of a notices region |
| **go(path)** | Change location | `kv.set("ui:nav", …)` plus optional morph — **not** an undeclared `nav.*` pair |
| **follow_up(event, action)** | After this event, run that Action | Host-issued continuation (pre-minted Cap). Peer fills slots only |
| **preview** | Instant local paint (pending, optimistic, coalesce) | Peer-local. Not an Op. Clears before apply |
| **use(*names)** | Enable stdlibs for this session | Load + agree + stamp + require drivers |
| **domain(...)** | Declare a product-specific pack | Register stdlib + driver; same handshake as bundled |

Helpers (`update`, `notify`, `go`) are **macros**. They expand to legal
pairs. They are not a second protocol and they are not the product story.
The product story is: **Actions return domain Ops**.

Preferred short verb for stdlibs: `app.use("search")`.
`use_domains` may exist as an alias; do not ship both as first-class docs.

---

## Banned in the public API

These came from noisy earlier designs or from sibling libraries.
Do not export them. Do not document them. Do not use them as internal
type names that leak into `__all__` or README examples.

| Banned | Why | Use instead |
|--------|-----|-------------|
| `chrome`, `chrome_pending`, `chrome_shadow` | cek-surface demo slang | `preview.pending`, `preview.update`, or automatic |
| `arm` | Implementation nickname | `follow_up` |
| `reply(*effects)` | Second IR next to Ops | `return [Op, …]` / `update` / `notify` / `go` |
| `Effect`, `KNOWN_KINDS` | Closed catalog that fights domains | Domain pairs + stamp |
| `Partial` | Invented type | `Component` |
| `shell` / `Frame` / `Main` as product types | Parallel layout DSL | `Layout`, one content region |
| `ceremony` | In-joke | “generated files” / CLI |
| `Interactive`, `controls()` | Adapter leakage | `on_click=`, `on_submit=` |
| `ActionResult(ok, flash, redirect)` | uxkit parallel result | `list[Op]` |
| `command` as substitute for Intent / Action | CEK rejected name | `Action` |
| `Surface` as the product type | Sibling library name | `App` |
| `plan()` as a wire IR | Composition is Python | `return [Op, …]` |
| `VStack` / SwiftUI wrappers as the product | Cargo-cult | ux-dom tags + Components |
| Any `s-*` CSS class system | Parallel to Tailwind | Tailwind utilities |
| `signal_set` as a domain | Macro only, if kept | `Op("kv", "set", …)` or a real stamped pair |

Internal adapter code may mention Channel types. It must not leak those
names into `__all__`.

Tutorial gloss once is allowed (“a Cap is a permission ticket”). A second
official term is not.
