# Lattice

A minimalist puzzle game. Draw straight lines between dots on a 6×6 lattice, starting at the green dot and ending at the red one. Slice every coloured circle without your lines crossing, in as few lines as possible.

Play it: https://antipastamasta.github.io/LatticeGame/ (on iPhone, open in Safari, then Share → Add to Home Screen).

## Files

- `src/game.html`: the whole game (markup, styles and scripts). This is the source to edit.
- `build.py`: wraps `src/game.html` into `index.html` with the phone settings (viewport, safe areas, Home Screen icon, full-screen mode). Run `python3 build.py` after editing.
- `index.html`: the built page that GitHub Pages serves. Don't edit it by hand.
- `manifest.webmanifest`, `icon-*.png`: Home Screen app name and icons.

The first `<script>` in `src/game.html` holds the game rules, puzzle generator and solver with no DOM code, so it can be reused in a native app.

## Free version

There are 5 fixed puzzles per difficulty (`FREE_SEEDS`), then a one-time unlock (`PRICE_LABEL`) gives endless generated puzzles. The purchase is simulated for now.

Planned: ship as an iOS and Android app by wrapping this page with Capacitor.
