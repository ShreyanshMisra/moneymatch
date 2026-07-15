# Phase 4 — Solo Pools & Tournaments

**Objective:** the two async formats (they absorb thin H2H liquidity — see
`docs/business/business-and-competition.md` §4), ported server-side with
**server-fetched telemetry only**. The PoC's "I cleared it / I missed" buttons
and client-posted scores do **not** survive this port.

**Depends on:** Phase 3 (worker, wallet, adapters). Parallel with Phase 5.

---

## Scope decisions (settled)

- **Games:** pools and tournaments ship for **CS2 only** at MVP (FaceIt is the
  one adapter with rich server-fetchable telemetry — K/D, ADR, HS%, kills;
  matches the design PDF, which is CS2-themed). Chess accuracy pools and Dota
  pools are post-MVP (chess needs game-analysis fetching; Dota telemetry is
  present but thin). The engine stays game-agnostic — this is config, not code.
- **Tournament format:** `leaderboard_pool` only ("play your normal matches
  during the window — your best stat is recorded automatically", PDF p.6). The
  PoC's simulated single-elim bracket is a demo artifact — cut it; a real
  bracket needs scheduling machinery that isn't MVP.
- **Pool tiers:** three standing tiers per the design (Easy/Hard/Brutal) with
  thresholds seeded from FaceIt stat distributions (the PoC FaceIt Lab
  distribution logic is the reference). Pools are **windowed rooms**: entrants
  join an OPEN room; room locks at window start; graded on your first finished
  match inside the window.
- **No bots.** PoC bot seeding is gone. Empty rooms display honestly
  ("3 playing"). Min-entrants (2 for pools) not met at lock → cancel + refund.

## Deliverables

1. Migrations: `solo_pools`, `solo_entries`, `tournaments`, `tournament_entries`
   (per `01-architecture.md` §2).
2. **Pool engine** ported from `poc-reference/api/_lib/solo_challenge.py`:
   geo-fence-before-escrow (reads `geo_config`), idempotent entry, grading
   (`grade_entry` compound-standard logic as-is), settlement invariant
   (clearers split pool − rake; none clear → full refund, zero rake;
   unverifiable → refund off the top). Floats → cents; remainder → rake.
3. **Tournament engine** ported from `poc-reference/api/_lib/tournament.py`
   (leaderboard paths only): ranking, prize-split renormalization, refunds.
   Scoring = **best qualifying stat during the window** across the entrant's
   finished matches (not a client-posted score).
4. **Worker extensions**: at window end, for each entrant fetch telemetry
   server-side via the adapter (`poll_eligible_games` within the window →
   `norm_to_telemetry`), grade, settle, reconcile, notify. During the window,
   refresh live tournament standings on a 10-min cadence (cached, cheap).
5. Room/tournament **scheduling**: a small seeder the worker runs — keep N open
   rooms per tier rolling (e.g. 6 h windows) and a weekend tournament per
   metric (the design's "Weekend ADR Rush"). Config-driven templates.
6. Endpoints: `/pools*`, `/tournaments*` from `01-architecture.md` §4; entries
   escrow through `wallet_service` with all Phase 1 checks.
7. **Pools screens** (PDF p.4–5): New pool (tier cards + slip with estimated
   multiplier + "Clear it and win" + Find pool) and Open pools (rooms with
   "N playing" + Enter). Multiplier copy per `02-design-system.md` §4
   (**estimated**, share-of-pool language — legal-critical).
8. **Tournament screen** (PDF p.6): cards with prize pool, 1st/2nd/3rd split,
   progress bar, JOINED chip; right-slip live standings with you highlighted;
   settled view with final standings + payouts.
9. Activity feed extended with pool/tournament rows.

## Reuse from `poc-reference/`

| What | From | Change |
| --- | --- | --- |
| Pool engine + geo-fence | `api/_lib/solo_challenge.py` | port; drop bot seeding + client telemetry |
| Tournament engine | `api/_lib/tournament.py` | leaderboard paths only; drop bracket sim + `genScore` |
| Invariant test suite | `tests/test_tournament.py` | port fully — it is the settlement spec |
| MetricTarget/MetricKind shapes | `api/_lib/schemas.py` | CS2 metrics only at MVP |
| Tier threshold derivation | FaceIt Lab distribution route in `api/index.py` (`/api/dev/faceit/distribution`) | becomes an offline/admin seeder script |
| Pool/tournament copy helpers | `frontend/src/utils/soloText.ts`, `tournamentText.ts` | adapt to new design language |

## Tests required

- Ported invariant suite green on cents: every settlement branch
  (`sum(payouts) + rake == sum(entries)`), renormalized splits, refund paths.
- Grading: compound standards (K/D **and** ADR **and** HS% **and** kills),
  missing telemetry → refund never fail, window-boundary matches excluded.
- Geo-fence: excluded-state user blocked at enter (403) **before** any ledger
  write; allowed after `geo_config` change without deploy.
- Worker: entrants with/without qualifying matches mixed in one room settle
  correctly; tournament best-of-window scoring picks the max, not the last.
- e2e: enter a pool → fixture telemetry clears it → payout equals share of pool.

## Exit criteria

- [ ] A CS2 user enters an Easy room, plays (fixture) FaceIt match, is graded
      from server-fetched telemetry, and is paid their pool share — with zero
      client input after "Enter".
- [ ] No self-report control exists anywhere in the UI or API.
- [ ] Tournament completes a full weekend window with live standings and
      correct split payouts.
- [ ] Rooms/tournaments roll over automatically via the seeder.
