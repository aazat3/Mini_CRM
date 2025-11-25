from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import *
from app.schemas import *

async def get_or_create_lead(session: AsyncSession, external_lead_id: int, name: str | None = None) -> Lead:
    q = await session.execute(
        select(Lead).where(Lead.external_lead_id == external_lead_id)
    )
    lead = q.scalar_one_or_none()

    if lead:
        return lead

    lead = Lead(external_lead_id=external_lead_id, name=name)
    session.add(lead)
    await session.flush()
    return lead