from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app.schemas import *
from app.DAO import stats_dao


router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/operators") # Операторы с количеством обращений
async def operator_stats(session: AsyncSession = Depends(get_session)):
    return await stats_dao.operator_stats(session)

@router.get("/sources") # Источники с количеством обращений 
async def source_stats(session: AsyncSession = Depends(get_session)):
    return await stats_dao.source_stats(session)

@router.get("/distribution/operators") # Операторы с обращениями
async def get_operator_distribution(
    session: AsyncSession = Depends(get_session)
):
    return await stats_dao.get_operator_distribution(session)