"""Feature-flag reads.

Flags live in the `feature_flags` DB table (00-README §3.10) so admins can flip
them without a deploy. This module is the read path; the write path arrives with
the admin surface in Phase 6.
"""

from __future__ import annotations

import structlog
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import (
    FLAG_QUEUE_PAUSED,
    FLAG_SETTLEMENT_PAUSED,
    REGISTERED_GAMES,
    game_flag_key,
)

log = structlog.get_logger(__name__)

# Fallback used before the table exists / when the DB is unreachable, so /health
# stays a liveness probe rather than a DB dependency.
DEFAULT_FLAGS: dict[str, bool] = {
    FLAG_QUEUE_PAUSED: False,
    FLAG_SETTLEMENT_PAUSED: False,
    **{game_flag_key(g): True for g in REGISTERED_GAMES},
}


async def get_boolean_flags(session: AsyncSession) -> dict[str, bool]:
    """Return the boolean feature flags, falling back to defaults on error."""
    try:
        from ..models.feature_flag import FeatureFlag

        result = await session.execute(select(FeatureFlag))
        rows = result.scalars().all()
    except SQLAlchemyError as exc:
        log.warning("feature_flags.read_failed", error=str(exc))
        return dict(DEFAULT_FLAGS)

    flags = dict(DEFAULT_FLAGS)
    for row in rows:
        flags[row.key] = bool(row.enabled)
    return flags
