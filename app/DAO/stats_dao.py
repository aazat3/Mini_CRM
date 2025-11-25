from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload


from app.models import *
from app.schemas import *

async def operator_stats(session: AsyncSession):
    q = await session.execute(
        select(
            Operator.id,
            Operator.name,
            func.count(Contact.id)
        ).join(Contact, isouter=True)
         .group_by(Operator.id)
         .order_by(Operator.id)
    )

    return [
        {"operator_id": row[0], "name": row[1], "contacts": row[2]}
        for row in q.all()
    ]

async def source_stats(session: AsyncSession):
    q = await session.execute(
        select(
            Source.id,
            Source.name,
            func.count(Contact.id)
        ).join(Contact, isouter=True)
         .group_by(Source.id)
         .order_by(Source.id)
    )

    return [
        {"source_id": row[0], "name": row[1], "contacts": row[2]}
        for row in q.all()
    ]

async def get_operator_distribution(session: AsyncSession):
    query = (
        select(Operator)
        .options(
            joinedload(Operator.contacts).joinedload(Contact.source),
        )
    )
    result = await session.execute(query)
    operators = result.unique().scalars().all()

    return operators