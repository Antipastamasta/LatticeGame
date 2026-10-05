# Lattice: handoff notes for Claude

Read this first in any new session. It holds what the code alone doesn't tell you: decisions, preferences and where the launch stands. Keep it current when any of that changes.

## The project

Lattice is a minimalist puzzle game by Michael (GitHub `Antipastamasta`), published under his single-member company **Lone Light Gaming LLC**. On a 6×6 lattice of dots, the player draws straight lines from the green dot to the red dot. Every coloured circle must be sliced, lines may not cross, and the goal is the fewest lines (par).

- Live web version (GitHub Pages, `main` branch root): https://antipastamasta.github.io/LatticeGame/ (the path is case-sensitive)
- Playable Claude artifact: https://claude.ai/artifact/2cFxVN2XhduRwnKXFtu1jw. Its source is `src/game.html` exactly (in the Claude project it also lives at `/mnt/project-files/lattice-demo/index.html`).
- Publishing guide (Claude Doc, Apple first): https://claude.ai/code/artifact/0e0339c6-9327-4e78-8ba8-5e1acbf959d9

Michael works on a Windows PC with no Mac and tests on his iPhone. He is new to app publishing, so explain steps plainly and click by click.

## How to work on it

- **Push every change to `main`** as soon as it is made, and republish the artifact when `src/game.html` changes (Michael's standing rule).
- Edit only `src/game.html` for the game, then run `python3 build.py`. Never hand-edit `index.html` or `www/`.
- Game rules, generator and solver live in the first `<script>` of `src/game.html` and must stay DOM-free.
- Don't change the sounds or the haptics feel without being asked. Michael approved them after many rounds: soft hollow wooden "tok" clicks (tenor, no noise), pentatonic chimes, no swish/hiss/snare textures anywhere. Sounds are synthesized in the `SFX` script; haptics are in `HAPTIC`.
- Fixed decisions: grid locked at 6×6 (keep the resize logic in code); par ranges Easy 2-4, Medium 3-5, Hard 4-6, Expert 5-7; the difficulty picker sits inline with the Lines, Par and Left stats; title screen has Play and How to play with no tagline; How to play is an animated slideshow.

## Files

| Path | What it is |
| --- | --- |
| `src/game.html` | The whole game (markup, styles, scripts). The source to edit. |
| `build.py` | Wraps `src/game.html` into `index.html` (web) and `www/index.html` (app bundle). Swaps Google Fonts for `fonts/`. |
| `index.html` | Built page GitHub Pages serves. Committed. |
| `www/` | Built app bundle. Not committed; Codemagic builds it. |
| `fonts/` | Bricolage Grotesque and IBM Plex Mono (latin woff2) with their SIL OFL licenses. |
| `privacy.html`, `support.html`, `pages.css` | Store-required pages on GitHub Pages. |
| `capacitor.config.json`, `package.json` | Capacitor 8 app setup (app ID `com.lonelightgaming.lattice`). |
| `ios/` | Native iOS project (Swift Package Manager, no CocoaPods). iPhone only, portrait only. |
| `assets/` | Icon source (`icon.svg`, rendered to `icon-only.png` 1024px) and plain splash images for `npx capacitor-assets generate --ios`. |
| `codemagic.yaml` | Cloud build: signs the iOS app and uploads it to TestFlight. |

## Business model and purchases

Free: 5 fixed puzzles per difficulty (`FREE_SEEDS`, 20 total). A one-time **non-consumable** purchase unlocks endless generated puzzles.

- Web: the unlock is pretend (`PRICE_LABEL` "$2.99"); a "Back to free version (testing)" link relocks it.
- App: the `STORE` module in `src/game.html` calls the RevenueCat Capacitor plugin through `window.Capacitor.Plugins.Purchases`. It shows the store's local price, buys, restores, and on launch re-checks ownership with the store. The testing relock link is hidden in the app.
- IDs that must never change once uploaded: bundle ID `com.lonelightgaming.lattice`, product ID `lattice_full_unlock`, RevenueCat entitlement `full`.
- `RC_KEY_IOS` / `RC_KEY_ANDROID` in `src/game.html` are RevenueCat's **public** SDK keys (safe in the repo). They are empty until Michael sets up RevenueCat; until then the app says "The store isn't set up yet."

## Tooling decisions

- Capacitor 8 wraps the web game. Codemagic (free tier, 500 macOS minutes a month) builds iOS in the cloud because Michael has no Mac. RevenueCat handles purchases (free under $2,500 a month). Ionic Appflow was ruled out (shutting down).
- Apple requires Xcode 26 / iOS 26 SDK for uploads (since April 28, 2026); `codemagic.yaml` uses `xcode: latest`.
- Android comes after the iPhone launch. Register Google Play as an **organization** under the LLC: personal accounts must run a 12-tester, 14-day closed test, organization accounts don't. Android must target API 36. Run `npx cap add android` then.

## Launch status (update as steps finish)

Done:
- Apple Developer membership exists, owned by Lone Light Gaming LLC (organization account).
- iOS project, real purchase flow, icon, splash, fonts, Codemagic file, privacy and support pages (October 2026).

Waiting on Michael:
- He is moving. He will update the LLC address with Dun & Bradstreet and open a business bank account, then do Apple's bank, tax (W-9) and Small Business Program forms.
- Sign up for Codemagic (with GitHub) and RevenueCat.
- A support email address for `support.html` (currently the placeholder `SUPPORT_EMAIL`).
- Check the name "Lattice" on the App Store and in USPTO search; fallback "Lattice: Line Puzzle".

## App Store setup (Michael's clicks, in order)

1. developer.apple.com > Certificates, IDs & Profiles > Identifiers > + > App ID `com.lonelightgaming.lattice` (In-App Purchase is on by default).
2. App Store Connect > Users and Access > Integrations > App Store Connect API > + key with App Manager role. Download the .p8 once and note the Key ID and Issuer ID.
3. Codemagic > Team settings > Integrations > Developer Portal: add that key, named exactly `Lattice App Store Connect`.
4. Codemagic > Team settings > codemagic.yaml settings > Code signing identities > iOS certificates > Generate certificate (Apple Distribution, that key). Download it, then upload it on the Upload tab with its password.
5. developer.apple.com > Profiles > + > App Store Connect distribution, for the App ID and the Codemagic certificate. Then Codemagic > iOS provisioning profiles > Fetch profiles and download it.
6. App Store Connect > Apps > + New App with that bundle ID. Monetization > In-App Purchases > Non-Consumable `lattice_full_unlock` at $2.99, display name "Endless puzzles".
7. App Store Connect > Integrations > In-App Purchase key: create one for RevenueCat. In RevenueCat add the Apple app (bundle ID + that key), entitlement `full` with the product attached, default offering. Copy the Apple public SDK key (`appl_…`) into `RC_KEY_IOS`.
8. Codemagic > Start new build > "iOS to TestFlight". Install TestFlight on the iPhone and test buying, deleting, reinstalling and restoring (sandbox purchases are free).
9. Listing: screenshots (6.9-inch iPhone), description, keywords, category Games > Puzzle, privacy URL `…/privacy.html`, support URL `…/support.html`, App Privacy answers (purchase history via RevenueCat, not used for tracking), age rating, then Add for Review.
