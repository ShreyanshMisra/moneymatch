"""Public health endpoint: service liveness + registered games + flags."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import __version__
from ..config import get_settings
from ..constants import REGISTERED_GAMES
from ..db.session import get_session
from ..schemas.health import HealthResponse
from ..services.feature_flags import get_boolean_flags

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(session: AsyncSession = Depends(get_session)) -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        env=settings.env,
        version=__version__,
        games=list(REGISTERED_GAMES),
        flags=await get_boolean_flags(session),
    )
