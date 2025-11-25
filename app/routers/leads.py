from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app.schemas import *
from app.DAO import leads_dao


router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/", response_model=list[LeadRead])
async def get_list_leads(session: AsyncSession = Depends(get_session)):
    return await leads_dao.get_list_leads(session=session)
