# Phase 4 brief — domains (first-class)

Follow [BUILD_PRODUCT_LIBRARY.md](../BUILD_PRODUCT_LIBRARY.md).
Sequence: [PLAN.md](../PLAN.md) Phase 4.

**Required seats:** Domain, Law, Channel, Adversary.

This is the product, not an add-on.

---

## Do

1. `app.use("search")` loads bundled stdlib, agrees, stamps, requires
   driver. Without a driver, doctor fails.
2. `app.domain(name, version, pairs, driver=...)` for product packs.
3. Structure validation (`validate_pair` rules).
4. Pair-identity tests: `("ui.dom","morph")` ok; `("ui","dom.morph")`
   illegal.
5. Cannot overwrite core `baseline` / `ui`. Empty `seed_pairs` illegal.
6. When `cek=require`, handshake goes through Channel's CEK adapter.
   When `cek=off`, the adapter still maintains a pair set.

## Corners

C-pre-18 … C-pre-23, C-pre-19 especially (Rust Peer kernel applies S
only).

## Exit

`use("search")` without a driver fails doctor; with a driver,
`Op("search","hits",…)` applies. A custom `orders.status` domain
works the same way.
