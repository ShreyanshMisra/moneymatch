"""Admin operator actions on users (09-phase-6 · deliverable 2).

Each mutation here is paired with an `admin_audit` row by its caller (the
`/admin/*` routers, or `scripts/grant_admin.py`). Functions flush, never commit —
the caller owns the transaction so the action and its audit row are atomic.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..errors import APIError
from ..models.user import USER_ROLES, User


class AdminActionError(APIError):
    """A rejected admin action (RFC-7807 via APIError)."""


async def get_user(session: AsyncSession, user_id: uuid.UUID) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise AdminActionError("user_not_found", "No such user.", status_code=404)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    return await session.scalar(select(User).where(User.username == username))


async def set_role(session: AsyncSession, user: User, role: str) -> User:
    """Set a user's role (`user` | `admin`). Grants are audited by the caller."""
    if role not in USER_ROLES:
        raise AdminActionError(
            "invalid_role",
            f"Role must be one of {USER_ROLES}.",
            status_code=422,
        )
    user.role = role
    await session.flush()
    return user
