"""Health-check response schema."""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    env: str
    version: str
    games: list[str]
    flags: dict[str, bool]
