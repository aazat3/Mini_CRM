from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app.schemas import *
from app.DAO import contacts_dao

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactRead)
async def create_contact(
    data: ContactCreate,
    session: AsyncSession = Depends(get_session)
):
    return await contacts_dao.create_contact(session=session, data = data)

@router.get("/", response_model=list[ContactRead])
async def get_list_contacts(session: AsyncSession = Depends(get_session)):
    return await contacts_dao.get_list_contacts(session)