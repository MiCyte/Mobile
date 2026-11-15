#!/usr/bin/env python3
"""The app's contract with the portal, checked before anything is built.

The portal knows the app by one thing, the user agent's `MiCyteApp/` suffix, and on that it
hides every purchase control (App Review 3.1.1). The web view may show two hosts and no
others; iOS enforces its own list (`WKAppBoundDomains`) and Capacitor a second one
(`allowNavigation`). All of it is configuration nothing else reads back, so a typo builds,
launches and screenshots exactly like the right thing. This fails the build instead.
"""
import json
import plistlib
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
MARK = "MiCyteApp/"  # what the portal looks for in the user agent


def problems() -> list[str]:
    config = json.loads((ROOT / "capacitor.config.json").read_text())
    with (ROOT / "ios/App/App/Info.plist").open("rb") as handle:
        plist = plistlib.load(handle)
    server = config.get("server") or {}
    allowed = sorted(server.get("allowNavigation") or [])
    bound = sorted(plist.get("WKAppBoundDomains") or [])
    start = urlsplit(server.get("url") or "")
    found = []
    if MARK not in (config.get("appendUserAgent") or ""):
        found.append(f"appendUserAgent does not carry {MARK!r}: the portal would treat the app as a browser")
    if start.scheme != "https" or start.hostname not in allowed:
        found.append(f"server.url {server.get('url')!r} is not an https page on an allowed host {allowed}")
    if allowed != bound:
        found.append(f"allowNavigation {allowed} and Info.plist WKAppBoundDomains {bound} differ")
    if (config.get("ios") or {}).get("limitsNavigationsToAppBoundDomains") is not True:
        found.append("ios.limitsNavigationsToAppBoundDomains is not true")
    # `npx cap sync ios` copies the configuration into the app; the copy is what ships.
    synced = ROOT / "ios/App/App/capacitor.config.json"
    if synced.exists():
        shipped = json.loads(synced.read_text())
        for key in ("appendUserAgent", "server", "ios"):
            if shipped.get(key) != config.get(key):
                found.append(f"the synced copy's {key!r} differs from capacitor.config.json; run `npx cap sync ios`")
    return found


if __name__ == "__main__":
    failed = problems()
    for line in failed:
        print(f"FAIL  {line}")
    if failed:
        sys.exit(1)
    print("the app's contract with the portal holds")
