# Lattice

A minimalist puzzle game. Draw straight lines between dots on a 6×6 lattice, starting at the green dot and ending at the red one. Slice every coloured circle without your lines crossing, in as few lines as possible.

Play it: https://antipastamasta.github.io/LatticeGame/ (on iPhone, open in Safari, then Share → Add to Home Screen).

**Working on this project (people or Claude): start with [CLAUDE.md](CLAUDE.md).** It holds the decisions, preferences, purchase setup and launch status.

## Files

- `src/game.html`: the whole game (markup, styles and scripts). This is the source to edit.
- `build.py`: builds `index.html` (the web page) and `www/` (the app bundle) from `src/game.html`. Run `python3 build.py` after editing.
- `index.html`: the built page that GitHub Pages serves. Don't edit it by hand.
- `privacy.html`, `support.html`: the privacy policy and support pages the App Store links to.
- `ios/`, `capacitor.config.json`, `package.json`: the iPhone app, built with Capacitor 8.
- `codemagic.yaml`: cloud build that signs the iPhone app and uploads it to TestFlight.
- `fonts/`: the game's fonts with their open font licenses. `assets/`: icon and splash sources.
- `manifest.webmanifest`, `icon-*.png`: Home Screen app name and icons for the web version.

The first `<script>` in `src/game.html` holds the game rules, puzzle generator and solver with no DOM code.

## Free version and unlock

There are 5 fixed puzzles per difficulty (`FREE_SEEDS`), then a one-time unlock gives endless generated puzzles. On the web the purchase is simulated; in the app it is a real App Store purchase through RevenueCat.
