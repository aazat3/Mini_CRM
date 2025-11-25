import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, Sequence, select


from app.models import *
from app.schemas import *

async def get_operator_load(session: AsyncSession, operator_id: int) -> int:
    q = await session.execute(
        select(func.count(Contact.id))
        .where(Contact.operator_id == operator_id)
        .where(Contact.is_active == True)
    )
    return q.scalar_one()


async def choose_operator(session: AsyncSession, source_id: int):
    rows = (
        await session.execute(
            select(OperatorSourceWeight, Operator)
            .join(Operator, Operator.id == OperatorSourceWeight.operator_id)
            .where(OperatorSourceWeight.source_id == source_id)
        )
    ).all()

    if not rows:
        return None

    candidates = []
    weights = []

    for osw, operator in rows:
        load = await get_operator_load(session, operator.id)

        if operator.is_active and load < operator.leads_limit:
            candidates.append(operator)
            weights.append(osw.weight)

    if not candidates:
        return None

    chosen = random.choices(candidates, weights=weights, k=1)[0] # Выбирает случайно на основе веса 
    return chosen

