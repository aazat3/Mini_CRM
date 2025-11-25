from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import *
from app.schemas import *
from app.DAO import leads_dao, distribution_service


async def create_contact(session: AsyncSession, data: ContactCreate) -> Contact:
    # 1. найти / создать лида
    lead = await leads_dao.get_or_create_lead(session=session, external_lead_id=data.external_lead_id)

    # 2. проверить источник
    q = await session.execute(select(Source).where(Source.id == data.source_id))
    source = q.scalar_one_or_none()
    if not source:
        raise HTTPException(404, "Source not found")

    # 3. выбрать оператора
    operator = await distribution_service.choose_operator(session, data.source_id)

    # 4. создать обращение
    contact = Contact(
        external_lead_id=lead.external_lead_id,
        source_id=data.source_id,
        operator_id=operator.id if operator else None,
        message=data.message,
    )

    session.add(contact)
    await session.commit()
    await session.refresh(contact)

    return contact


async def get_list_contacts(session: AsyncSession, limit: int = None) -> list[Contact]:
    stmt = select(Contact)
    if limit:
        stmt = stmt.limit(limit=limit)
    q = await session.execute(stmt)
    return q.scalars().all()