"""Admin surface schemas (09-phase-6).

The admin API is a plain, dense operator surface — not the consumer design
system. These models still go through Pydantic → OpenAPI → the generated TS
client so the admin web tables stay type-safe.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

# --------------------------------------------------------------------------- #
# Flags
# --------------------------------------------------------------------------- #


class FlagItem(BaseModel):
    key: str
    enabled: bool
    payload: dict[str, Any] = Field(default_factory=dict)


class FlagsResponse(BaseModel):
    flags: list[FlagItem]


class UpdateFlagRequest(BaseModel):
    """Patch a flag: toggle `enabled` and/or replace its `payload` (e.g.
    `geo_config`'s excluded-state list). At least one field must be present."""

    enabled: bool | None = None
    payload: dict[str, Any] | None = None
