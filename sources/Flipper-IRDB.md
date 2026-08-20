# Flipper-IRDB source

Upstream repository: `Lucaslhm/Flipper-IRDB`.

HomeController DeviceDB imports only TV and A/C captures that can be represented by the current HomeController runtime (supported parsed protocols or complete raw timing patterns) and that pass minimum usefulness checks. Generated model JSON files retain the upstream relative path in `sources`.

The upstream repository currently contains a `LICENSE` file declaring **CC0 1.0 Universal**. The import workflow does not assume that a sparse capture is complete or model-verified; imported records are labelled `community-capture` unless promoted to the curated set after stronger evidence/testing.

Curated HomeController definitions override generated records when the same device is known more precisely.
