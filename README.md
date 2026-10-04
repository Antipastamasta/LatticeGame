# Lattice

A minimalist puzzle game. Draw straight lines between dots on a 6×6 lattice, starting at the green dot and ending at the red one. Slice every coloured circle without your lines crossing, in as few lines as possible.

- `index.html` is the whole game: one self-contained page with no build step and no server. Open it in a browser to play.
- The first `<script>` block holds the game rules, puzzle generator and solver, with no DOM code, so it can be reused in a mobile app.
- Free version: 5 fixed puzzles per difficulty (`FREE_SEEDS`), then a one-time unlock (`PRICE_LABEL`) for endless generated puzzles. The purchase is simulated for now.

Planned: ship as an iOS and Android app by wrapping this page with Capacitor.
