# HomeController Bluetooth knowledge base

`bluetooth/profiles/` is the authoritative model/protocol knowledge base for normal BLE devices supported by HomeController.

## Ownership boundary

- **HomeController runtime** owns generic Bluetooth transport, matching, profile execution, primitive decoding, validation, diagnostics and fallback Learning.
- **HomeController-DeviceDB** owns device/model knowledge: match signatures, field definitions, protocol operations, versions and provenance.
- Normal device support must not require a model-specific branch in discovery or UI code. Add or update a profile here unless the protocol genuinely requires a new reusable runtime primitive/protocol-family adapter.

## Profile lifecycle

Profiles use `schemas/ble-profile-v1.schema.json`. Published files are immutable by version: use `<profile-id>-vN.json` and increment `version` when protocol knowledge changes. `bluetooth/profiles/index.json` is the catalog consumed by HomeController and contains the active profile version, minimum runtime version, SHA-256 and status.

Statuses:

- `experimental`: protocol definition is still being validated on hardware/test vectors.
- `stable`: verified sufficiently for normal automatic recognition/use.
- `deprecated`: retained for history/migration but should not be selected as current support.

`minimumRuntimeVersion` must be raised when a profile needs a decoder primitive or operation unavailable in older HomeController runtimes.

## Provenance

Every profile must contain `source.name` and `source.url`. `source.license` and `source.notes` should describe where protocol facts came from and any important independent implementation notes. External projects such as Theengs are research inputs; their implementation code is not embedded into HomeController.

## Publishing checklist

1. Create a versioned profile JSON and validate it against `ble-profile-v1.schema.json`.
2. Make match rules specific enough to avoid unrelated-device false positives.
3. Record provenance.
4. Add deterministic raw-input -> decoded-output test vectors under `bluetooth/test-vectors/`.
5. Verify the profile against hardware or reliable captures when possible.
6. Compute the exact profile file SHA-256 and put it in `bluetooth/profiles/index.json`.
7. Increment `catalogVersion` whenever the published catalog changes.
8. Mark `stable` only after verification; otherwise publish as `experimental`.

## Runtime resolution

HomeController resolves BLE data through standardized Bluetooth SIG semantics where applicable, then DeviceDB profile matching/execution, and finally safe unknown-device probing/Learning when no known profile matches. Device-specific knowledge belongs here, not in the normal discovery page.
