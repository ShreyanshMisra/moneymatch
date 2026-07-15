# Backlog (post-MVP / discovered during build)

Items discovered mid-phase that are out of that phase's scope land here with a
one-line rationale. Seeded with known post-MVP work:

- **OAuth account binding** (Lichess OAuth, FaceIt OAuth2, Steam OpenID) —
  replaces username-claim; prerequisite for anything beyond internal beta
  (integrity audit #5, #6). Targeted Lichess challenges bound to both accounts.
- **Spectate/tracker panels** — port `poc-reference/api/_lib/spectate.py` /
  `tracker.py` + PoC hooks for a live match detail view in Activity.
- **Chess accuracy + Dota solo pools** — needs server-side analysis fetching /
  richer telemetry; engine already game-agnostic.
- **Single-elim bracket tournaments** — real scheduling machinery.
- **Email + push notifications** — `notifications.channel_sent` is ready.
- **Mobile layout pass** — the PDF is desktop-only.
- **Marketing/landing page + waitlist** — gtm-prelaunch.md §2.
- **Host cheat-flag ingestion + clawback** — gems-phase integrity item.
- **Smurf floors** (min account age / rated games / non-provisional rating)
  before public launch.
- **SSE for live surfaces** — replace polling where it hurts.
