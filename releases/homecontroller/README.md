# HomeController Android releases

This public folder is the update channel for the private `sicsalad/HomeController` application repository.

- `version.json` is the stable machine-readable update manifest used by the app.
- The APK itself is published as the `HomeController-latest.apk` asset on the public GitHub Release tagged `homecontroller-latest`.
- Each successful signed Android build updates the release asset and then updates `version.json`.

The APK must always be signed with the same persistent Android signing key and have an increasing Android `versionCode`, otherwise Android cannot install it as an in-place update.
