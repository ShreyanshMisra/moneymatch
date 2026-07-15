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

## Running it locally

Prerequisites: **Docker**, **Node 20+** with `pnpm` (via `corepack enable pnpm`),
and [**uv**](https://docs.astral.sh/uv/) for the Python API.

```bash
# 1. Configure env (fill in the Supabase keys — see the Supabase note below).
cp .env.example .env

# 2. Install all dependencies (pnpm workspace + API venv).
make install

# 3. Start Postgres + API + web together.
make dev
```

Then open http://localhost:5173, sign in with Google or email, complete
onboarding (username + state + 18+), and land on the Play screen.

Individual pieces (each reads the root `.env`):

| Command                        | What it does                                      |
| ------------------------------ | ------------------------------------------------- |
| `make db`                      | Start Postgres (Docker) and wait until healthy    |
| `make migrate`                 | Apply Alembic migrations                          |
| `make api`                     | Run the FastAPI service on :8000 (reload)         |
| `make web`                     | Run the Vite dev server on :5173                  |
| `make test`                    | Run API (pytest) + web (vitest) suites            |
| `make lint` / `make typecheck` | ruff/prettier + mypy/tsc                          |
| `make gen-api`                 | Regenerate the TS API client from the running API |
| `make help`                    | List all commands                                 |

**Supabase:** create a project, enable Email + Google auth, and copy the project
URL, JWT secret, and publishable/anon key into `.env` (`SUPABASE_*` and
`VITE_SUPABASE_*`). The API verifies Supabase JWTs and owns all other state; the
browser never touches the database.

**Port note:** if `5432` is already taken, set `DB_PORT` in `.env` and update the
port in `DATABASE_URL` to match.

## Repo layout

```
apps/web            React + Vite SPA (talks only to the API)
apps/api            FastAPI service (owns every number; verifies Supabase JWTs)
packages/api-client Generated TypeScript client (OpenAPI → TS)
docs/               Implementation guide, product, legal, design
poc-reference/      Frozen PoC — reference only, never imported
```

## Status

Phase 0 (foundation) complete: monorepo, CI, local Postgres, Supabase auth with
server-side user provisioning, the app shell, and the sign-in/onboarding flow.
Next: Phase 1 — wallet & ledger.

## Invariants (memorize these)

1. `sum(payouts) + rake == sum(entries)` on every settlement path.
2. The server owns every number — no client-supplied amounts, timestamps,
   telemetry, or results.
3. Settlements are host-API-verified. No self-reporting, no screenshots.
4. Rake only when a prize distributes; refunds and pushes rake nothing.
5. Money is integer cents.
