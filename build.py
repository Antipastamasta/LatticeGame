#!/usr/bin/env python3
"""Build the web page and the app's web bundle from src/game.html.

src/game.html is the page body as published to the Claude artifact (no <html>/<head> of its own,
fonts from Google Fonts). This wraps it in a full document with the mobile and safe-area settings
a phone needs, swaps Google Fonts for the copies in fonts/, and writes:

- index.html          the page GitHub Pages serves (adds the Home Screen icon and manifest)
- www/index.html      the bundle Capacitor copies into the iOS and Android apps (with fonts/)
"""
import re
import shutil
from pathlib import Path

root = Path(__file__).parent
game = (root / "src" / "game.html").read_text()
cut = game.index("<style>")
head_extra, body = game[:cut].strip(), game[cut:]

# Google Fonts links -> the same fonts served from fonts/ (works offline in the app)
head_extra = re.sub(r'<link rel="(preconnect|stylesheet)" href="https://fonts\.(googleapis|gstatic)\.com[^>]*>\n?', "", head_extra).strip()
LATIN = ("U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, "
         "U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")
FONTS = f"""@font-face {{ font-family: "Bricolage Grotesque"; font-style: normal; font-weight: 500 700; font-display: swap; src: url(fonts/bricolage-grotesque-latin.woff2) format("woff2"); unicode-range: {LATIN}; }}
@font-face {{ font-family: "IBM Plex Mono"; font-style: normal; font-weight: 400; font-display: swap; src: url(fonts/ibm-plex-mono-400-latin.woff2) format("woff2"); unicode-range: {LATIN}; }}
@font-face {{ font-family: "IBM Plex Mono"; font-style: normal; font-weight: 500; font-display: swap; src: url(fonts/ibm-plex-mono-500-latin.woff2) format("woff2"); unicode-range: {LATIN}; }}"""

WEB_HEAD = """<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Lattice">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">"""

# in the app: no text selection, callouts or phone-number links, like a native screen
APP_HEAD = '<meta name="format-detection" content="telephone=no">'
APP_CSS = "body { -webkit-user-select: none; user-select: none; -webkit-touch-callout: none; overscroll-behavior: none; }"


def page(extra_head, extra_css=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f6f7f5">
{extra_head}
{head_extra}
<style>
{FONTS}
:root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); touch-action: manipulation; }}
body {{ margin: 0; font: 14px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif; background: #f6f7f5; -webkit-tap-highlight-color: transparent; -webkit-text-size-adjust: 100%; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
{extra_css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


(root / "index.html").write_text(page(WEB_HEAD))

www = root / "www"
if www.exists():
    shutil.rmtree(www)
(www / "fonts").mkdir(parents=True)
(www / "index.html").write_text(page(APP_HEAD, APP_CSS))
for f in (root / "fonts").iterdir():
    shutil.copy(f, www / "fonts" / f.name)
print("wrote index.html and www/")
