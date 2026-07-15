# Phase 5 — Social & Retention Surfaces

**Objective:** friends, direct challenges + invite links, the Inbox, and the
Leaderboard — the liquidity and return-trigger layer (a P2P platform must be
able to *summon* opponents; see `docs/business/business-and-competition.md` §3).

**Depends on:** Phase 3. Parallel with Phase 4.

---

## Deliverables

1. Migrations: `friendships`, `challenges`, (extend) `notifications`.
2. **Friends service + endpoints**: add by username, request/accept/decline,
   presence-lite (`last_seen_at` heartbeat on API activity; green dot =
   active in last 5 min). No chat at MVP.
3. **Challenges** (the design's "Invite friend" slip + Friends "Challenge" pill):
   - Direct: challenger picks market + entry preset → challengee gets an inbox
     notification + Respond → accept creates a `match` (PENDING) through the
     same lifecycle service (both confirm → escrow → activate). Same
     `can_pair` checks as the queue **except** the 24 h repeat-pair cooldown is
     relaxed for explicit friend challenges at demo-money MVP (flagged config;
     revisit before real money — rematch is a core loop but also the collusion
     surface).
   - **Invite link**: `POST /challenges` without a challengee returns
     `invite_token` + URL (`/i/{token}`). Public preview page (market, entry,
     challenger name) → sign-in/sign-up → link required game → accept. This is
     the acquisition loop from `docs/business/gtm-prelaunch.md` §3.2 — treat
     the funnel as first-class (instrument every step).
   - Expiry 24 h; decline/expire notifies the challenger.
4. **Inbox screen** (PDF p.11): notification rows (unread green dot, age,
   action pills — View → deep link to match/pool, Respond → challenge accept
   flow). Bell in sidebar shows unread dot. Mark-read on view.
5. **Leaderboard** (PDF p.7, under the Tournament section's sub-tabs):
   `GET /leaderboard` ranks **real users** by ROI (net / staked, ≥3 settled
   contests to qualify) over a rolling 30 days. The PoC's seeded bot field is
   gone. You-row highlighted. Port the ROI/ranking math from
   `poc-reference/api/_lib/leaderboard.py` + the PoC's client-side merge logic,
   but computed server-side from the ledger.
6. **Rematch**: one-tap rematch button on settled H2H rows in Activity —
   creates a challenge to the same opponent (subject to the same checks).
7. Notification fan-out consolidated: every lifecycle event writes
   `notifications` rows (match_found, settled, refund, challenge_received,
   challenge_accepted, friend_request, room_filled). Email/push are post-MVP;
   the table schema carries a `channel_sent jsonb` for it.

## Reuse from `poc-reference/`

| What | From | Change |
| --- | --- | --- |
| ROI leaderboard math | `api/_lib/leaderboard.py` | real users from ledger, not seeded bots |
| Head-to-head record display | PoC Profile "My Contests" (`frontend/src/hooks/useContracts.ts` derived lists) | becomes per-opponent record on Friends rows (optional) |
| Toast patterns | `frontend/src/hooks/useToasts.ts` | port |

## Tests required

- Friendship state machine (duplicate requests, blocked users, self-add rejected).
- Challenge: full accept path creates a correct PENDING match; decline/expiry
  notify; invite token is single-use, expires, and survives the
  sign-up-then-accept flow; challenge to an unlinked-game user prompts linking.
- Leaderboard: qualification threshold, ROI math against ledger fixtures,
  rolling window boundary.
- Notifications: unread counts; mark-read idempotent.
- e2e: user A sends invite link → user B (fresh signup) accepts → both confirm
  → fixture settle → both inboxes correct.

## Exit criteria

- [ ] Friends/Inbox/Leaderboard match PDF p.7, 8, 11.
- [ ] Invite-link funnel works for a brand-new user end-to-end and every step
      emits an analytics event.
- [ ] A settled match can be rematched in two clicks.
