#!/usr/bin/env python3
"""Build index.html for GitHub Pages from src/game.html.

src/game.html is the page body as published to the Claude artifact (no <html>/<head> of its own).
This wraps it in a full document with the mobile, Home Screen and safe-area settings a phone needs.
"""
from pathlib import Path

root = Path(__file__).parent
game = (root / "src" / "game.html").read_text()
cut = game.index("<style>")
head_extra, body = game[:cut].strip(), game[cut:]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Lattice">
<meta name="theme-color" content="#f6f7f5">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
{head_extra}
<style>
:root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); touch-action: manipulation; }}
body {{ margin: 0; font: 14px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif; background: #f6f7f5; -webkit-tap-highlight-color: transparent; -webkit-text-size-adjust: 100%; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""
(root / "index.html").write_text(page)
print("wrote index.html")
