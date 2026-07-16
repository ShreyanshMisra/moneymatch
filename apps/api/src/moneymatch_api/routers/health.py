"""Public health endpoint: service liveness + registered games + flags."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import __version__
from ..adapters import registry
from ..config import get_settings
from ..db.session import get_session
from ..schemas.health import HealthResponse
from ..services.feature_flags import get_boolean_flags

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(session: AsyncSession = Depends(get_session)) -> HealthResponse:
    settings = get_settings()
    flags = await get_boolean_flags(session)
    return HealthResponse(
        status="ok",
        env=settings.env,
        version=__version__,
        # Registered games come from the adapter registry, filtered by flags —
        # a disabled game:<id> flag drops the game here too (05-phase-2 · d.7).
        games=registry.enabled_ids(flags),
        flags=flags,
    )
