from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app.schemas import *
from app.DAO import sources_dao

router = APIRouter(prefix="/sources", tags=["sources"])

@router.post("/", response_model=SourceRead)
async def create_source(data: SourceCreate, session: AsyncSession = Depends(get_session)):
    return await sources_dao.create_source(session=session, data=data)


@router.post("/{source_id}/weights", response_model=OperatorSourceWeightRead)
async def set_operator_weight(
    source_id: int,
    data: OperatorSourceWeightCreate,
    session: AsyncSession = Depends(get_session)
):
    return await sources_dao.set_operator_weight(session=session, source_id = source_id, data=data)

@router.get("/", response_model=list[SourceRead])
async def get_list_sources(session: AsyncSession = Depends(get_session)):
    return await sources_dao.get_list_sources(session=session)