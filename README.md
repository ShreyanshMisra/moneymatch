# MoneyMatch

**Peer-to-peer skill wagering on games you already play.** Players stake equal
entries into an escrowed pot, play a real match on a connected game (Chess via
Lichess, CS2 via FaceIt, Dota 2 via OpenDota), results are auto-verified against
the host game's API, and the winner takes the pot minus a fixed, disclosed rake —
the platform's only revenue. Never house-banked, never odds-priced.

This repo is the **MVP build** (demo money, real everything else), developed
from the validated PoC in the `clutchbook` repo.

## Where things are

- **[`docs/implementation-guide/`](./docs/implementation-guide/00-README.md)** —
  the phased implementation plan (start at `00-README.md`). This is the
  authoritative guide for building the MVP in this repo.
- [`docs/design/moneymatch-design.pdf`](./docs/design/moneymatch-design.pdf) —
  the visual design source of truth.
- [`docs/`](./docs/README.md) — product, legal, and business docs (index inside).
- [`poc-reference/`](./poc-reference/README.md) — frozen copy of the PoC's
  reusable code and tests. **Reference only:** port from it, never import it.

## Status

Pre–Phase 0: documentation and migration baseline only. The application
scaffold lands with Phase 0 of the implementation guide, which also owns the
real run instructions that will replace this section.

## Invariants (memorize these)

1. `sum(payouts) + rake == sum(entries)` on every settlement path.
2. The server owns every number — no client-supplied amounts, timestamps,
   telemetry, or results.
3. Settlements are host-API-verified. No self-reporting, no screenshots.
4. Rake only when a prize distributes; refunds and pushes rake nothing.
5. Money is integer cents.
