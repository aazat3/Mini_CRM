from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


from app.models import *
from app.schemas import *


async def create_source(session: AsyncSession, data: SourceCreate) -> Source:
    src = Source(**data.model_dump())
    session.add(src)
    await session.commit()
    await session.refresh(src)
    return src

async def set_operator_weight(session: AsyncSession, source_id: int, data: OperatorSourceWeightCreate) -> OperatorSourceWeight:
    op_q = await session.execute(
        select(Operator).where(Operator.id == data.operator_id)
    )
    operator = op_q.scalar_one_or_none()
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")

    src_q = await session.execute(
        select(Source).where(Source.id == source_id)
    )
    source = src_q.scalar_one_or_none()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    
    q = await session.execute(
        select(OperatorSourceWeight)
        .where(
            OperatorSourceWeight.source_id == source_id,
            OperatorSourceWeight.operator_id == data.operator_id
        )
    )
    row = q.scalar_one_or_none()

    if row:
        row.weight = data.weight
    else:
        row = OperatorSourceWeight(
            operator_id=data.operator_id,
            source_id=source_id,
            weight=data.weight
        )
        session.add(row)

    await session.commit()
    return row

async def get_list_sources(session: AsyncSession, limit: int = None) -> list[Source]:
    stmt = select(Source)
    if limit:
        stmt = stmt.limit(limit=limit)
    q = await session.execute(stmt)
    return q.scalars().all()