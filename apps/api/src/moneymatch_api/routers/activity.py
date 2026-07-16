"""`/activity` — the unified activity feed (design Activity screen, PDF p.9).

Phase 3 surfaces head-to-head matches; pools and tournaments join the same feed
in Phase 4. Every number here is server-derived: your realized net comes from the
ledger-backed `payout_cents`, never from anything the client sent.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session
from ..dependencies import CurrentUser
from ..models.play import Match, MatchPlayer
from ..models.user import User
from ..schemas.play import ActivityItem, ActivityResponse
from ..services.markets import get as get_market
from ..services.match_states import CANCELED, PUSHED, SETTLED

router = APIRouter(tags=["activity"])

_TERMINAL = {SETTLED, PUSHED, CANCELED}
_DEFAULT_LIMIT = 50


@router.get("/activity", response_model=ActivityResponse)
async def get_activity(
    user: CurrentUser,
    limit: int = Query(default=_DEFAULT_LIMIT, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
) -> ActivityResponse:
    # The viewer's matches, newest first.
    match_rows = list(
        await session.scalars(
            select(Match)
            .join(MatchPlayer, MatchPlayer.match_id == Match.id)
            .where(MatchPlayer.user_id == user.id)
            .order_by(Match.created_at.desc())
            .limit(limit)
        )
    )
    if not match_rows:
        return ActivityResponse(items=[])

    match_ids = [m.id for m in match_rows]
    seats = list(
        await session.scalars(
            select(MatchPlayer).where(MatchPlayer.match_id.in_(match_ids))
        )
    )
    by_match: dict = {}
    for seat in seats:
        by_match.setdefault(seat.match_id, []).append(seat)

    opp_ids = [s.user_id for s in seats if s.user_id != user.id]
    names = {}
    if opp_ids:
        rows = await session.execute(
            select(User.id, User.username).where(User.id.in_(opp_ids))
        )
        names = {uid: uname for uid, uname in rows}

    items: list[ActivityItem] = []
    for match in match_rows:
        seat_pair = by_match.get(match.id, [])
        yours = next((s for s in seat_pair if s.user_id == user.id), None)
        opp = next((s for s in seat_pair if s.user_id != user.id), None)
        if yours is None:
            continue

        net = None
        if match.state in _TERMINAL:
            escrowed = match.entry_cents if yours.confirmed_at is not None else 0
            net = yours.payout_cents - escrowed

        market = get_market(match.game, match.market)
        items.append(
            ActivityItem(
                type="match",
                id=match.id,
                game=match.game,
                market=match.market,
                market_label=market.label if market else match.market,
                kind=market.kind if market else "",
                state=match.state,
                entry_cents=match.entry_cents,
                net_cents=net,
                opponent_username=names.get(opp.user_id) if opp else None,
                your_stat_line=yours.stat_line,
                opponent_stat_line=opp.stat_line if opp else None,
                created_at=match.created_at,
                resolved_at=match.resolved_at,
            )
        )
    return ActivityResponse(items=items)
