from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models import *
from app.schemas import *


async def create_operator(session: AsyncSession, data: OperatorCreate) -> Operator:
    op = Operator(**data.model_dump())
    session.add(op)
    await session.commit()
    await session.refresh(op)
    return op

async def get_list_operators(session: AsyncSession, limit: int = None) -> list[Operator]:
    stmt = select(Operator)
    if limit:
        stmt = stmt.limit(limit=limit)
    q = await session.execute(stmt)
    return q.scalars().all()

async def update_operator(session: AsyncSession, operator_id: int, data: OperatorUpdate) -> Operator:
    q = await session.execute(select(Operator).where(Operator.id == operator_id))
    op = q.scalar_one_or_none()
    if op is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(op, k, v)
    await session.commit()
    await session.refresh(op)
    return op
