# MiCyte for iPhone

The MiCyte app: your hosted [MiCyte](https://github.com/MiCyte/MiCyte) instance on your
phone. It opens the same dashboard as the web, at `https://micyte.com/dashboard/`, signed in
with the same account, inside a native shell built with [Capacitor](https://capacitorjs.com).
One project builds the iOS app now and the Android app later.

## What the app is, exactly

| Piece | Where |
|---|---|
| Start page | `https://micyte.com/dashboard/` (`capacitor.config.json`, `server.url`) |
| Sign-in | the hosted door's own sign-in page, inside the app; the web view keeps the session |
| Pages it may show | `micyte.com` and `auth.fruitfulnetworkdevelopment.com` only (app-bound domains); any other link opens in Safari |
| How the portal knows it is the app | the user agent ends in `MiCyteApp/<version>` |
| Native | pull down to reload, swipe back, an offline page (`www/offline.html`) |
| App links | `applinks:micyte.com` for `/app/*`, published at `https://micyte.com/.well-known/apple-app-site-association` |

**No selling in the app.** Plans are a digital service, so a card form or an upgrade button
inside an iOS app would need Apple's in-app purchase. The portal hides every purchase
control for the app's user agent; plans are bought on the website.

**Privacy.** The app has no analytics, no advertising and no tracking. What it declares is in
`ios/App/App/PrivacyInfo.xcprivacy` and on [micyte.com/privacy](https://micyte.com/privacy).

## Building

You need Node 22 and, for the iOS build itself, a Mac with Xcode 16 or later.

```sh
npm ci
npx cap sync ios
open ios/App/App.xcodeproj
```

Continuous integration does the same on GitHub's macOS runners:

* **iOS build** (every push and pull request): checks the app's contract with the portal
  (`ci/check_app_contract.py`: the user agent mark, and the two hosts the web view may
  show), builds for the simulator, launches the app and keeps a screenshot as an artifact.
  Needs no secrets.
* **TestFlight** (run by hand, or by pushing a `v*` tag): archives, signs with Xcode's
  automatic signing and uploads to App Store Connect. Needs three repository secrets from an
  App Store Connect API key: `ASC_KEY_ID`, `ASC_ISSUER_ID` and `ASC_KEY_P8` (the whole text of
  the `.p8` file). No certificate or profile is kept in this repository.

`resources/` holds the sources of the icon and the launch screen (`icon.svg`, `splash.svg`)
and their rendered PNGs.

## Contributing

Pull requests are welcome. Every commit carries a Developer Certificate of Origin sign-off
(`git commit -s`), checked on each pull request.

## License

AGPL-3.0-or-later. See `LICENSE`.
