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

# Feature-flag keys seeded in the first migration and readable/writable by admin.
FLAG_QUEUE_PAUSED = "queue_paused"
FLAG_SETTLEMENT_PAUSED = "settlement_paused"
FLAG_GEO_CONFIG = "geo_config"


# Per-game enable flags (game:<id>).
def game_flag_key(game_id: str) -> str:
    return f"game:{game_id}"
