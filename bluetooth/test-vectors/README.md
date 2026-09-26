# BLE profile test vectors

Deterministic test vectors accompany DeviceDB BLE profiles so protocol definitions can be checked without physical hardware.

Each profile should eventually have `<profile-id>-vN.json` in this directory. A vector describes the profile input selector, exact raw bytes and expected decoded fields. The runtime/test tooling may consume this format directly.

Example:

```json
{
  "schemaVersion": 1,
  "profileId": "example-sensor",
  "profileVersion": 1,
  "vectors": [
    {
      "name": "temperature sample",
      "input": { "kind": "characteristic", "serviceUuid": "181A", "characteristicUuid": "2A6E" },
      "rawHex": "C409",
      "expected": [ { "code": "temperature", "value": 25.0, "unit": "°C" } ]
    }
  ]
}
```

For `serviceData`, set `serviceUuid`; for `manufacturerData`, set `manufacturerId`; for `notification`, set service and characteristic UUIDs. A profile should include vectors for normal values plus useful boundary/sentinel/enum cases where applicable.

Test vectors are protocol evidence, not discovery heuristics. Matching correctness should be tested separately with representative device identities so broad name/service matches cannot silently create false positives.
