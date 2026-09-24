# BLE protocol profiles

Machine-readable BLE protocol knowledge lives here, separate from application code. Profiles describe matching, provenance, original protocol field codes and declarative decoding. A profile is not a HomeController device driver and must not invent semantic names when the source does not define them.

`index.json` is the versioned catalog consumed by the app. Profile payloads are integrity-checked with SHA-256 before they enter the local cache. No concrete device profile is added in this foundation commit.
