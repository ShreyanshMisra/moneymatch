"""Domain constants shared across the API.

Game ids are the canonical `<game>.<host>` identifiers used everywhere
(linked_accounts.game, markets, adapter registry keys).
"""

from __future__ import annotations

GAME_CHESS_LICHESS = "chess.lichess"
GAME_CS2_FACEIT = "cs2.faceit"
GAME_DOTA2_OPENDOTA = "dota2.opendota"

REGISTERED_GAMES: tuple[str, ...] = (
    GAME_CHESS_LICHESS,
    GAME_CS2_FACEIT,
    GAME_DOTA2_OPENDOTA,
)

# Human labels for the Profile "Linked games" rows (design PDF p.12).
GAME_DISPLAY_NAMES: dict[str, str] = {
    GAME_CHESS_LICHESS: "Chess — Lichess",
    GAME_CS2_FACEIT: "CS2 — FACEIT",
    GAME_DOTA2_OPENDOTA: "Dota 2 — OpenDota",
}


def game_display_name(game_id: str) -> str:
    return GAME_DISPLAY_NAMES.get(game_id, game_id)


# Feature-flag keys seeded in the first migration and readable/writable by admin.
FLAG_QUEUE_PAUSED = "queue_paused"
FLAG_SETTLEMENT_PAUSED = "settlement_paused"
FLAG_GEO_CONFIG = "geo_config"


# Per-game enable flags (game:<id>).
def game_flag_key(game_id: str) -> str:
    return f"game:{game_id}"


# --------------------------------------------------------------------------- #
# Metric-model config (05-phase-2 · deliverable 6).
# "Floors live in config, not code" — tune these here, never inline in the
# bootstrap logic. Metrics are the typed, rate-based allowlist only (never raw
# totals, never anything outside the player's control — 01-architecture §2).
# --------------------------------------------------------------------------- #

# Rate metrics we build EWMA skill models for, per game. Chess settles on `win`
# only, so it models no per-metric skill here.
GAME_RATE_METRICS: dict[str, tuple[str, ...]] = {
    GAME_CHESS_LICHESS: (),
    GAME_CS2_FACEIT: ("cs2_kd_ratio", "cs2_adr", "cs2_headshot_pct"),
    GAME_DOTA2_OPENDOTA: ("dota2_kda_ratio", "dota2_gpm"),
}

# EWMA recency weighting expressed as a half-life in matches.
METRIC_EWMA_HALF_LIFE = 10

# Below this per-metric sample size the metric is **provisional** — no stat
# duels / pool entries on it (challenge-engine proposal §3/§6).
METRIC_PROVISIONAL_MIN_N = 10

# Per-game finished-history floor. An account below it gets H2H `win` markets
# only (no stat duels), regardless of any single metric's n.
GAME_HISTORY_FLOOR: dict[str, int] = {
    GAME_CHESS_LICHESS: 20,  # rated games
    GAME_CS2_FACEIT: 25,  # matches
    GAME_DOTA2_OPENDOTA: 25,  # matches
}
