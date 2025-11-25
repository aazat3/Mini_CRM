from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app.schemas import *
from app.DAO import operators_dao


router = APIRouter(prefix="/operators", tags=["operators"])

@router.get("/", response_model=list[OperatorRead])
async def get_list_operators(session: AsyncSession = Depends(get_session)):
    return await operators_dao.get_list_operators(session)

@router.post("/", response_model=OperatorRead, status_code=status.HTTP_201_CREATED)
async def create_operator(data: OperatorCreate, session: AsyncSession = Depends(get_session)):
    return await operators_dao.create_operator(session, data=data)

@router.patch("/{operator_id}", response_model=OperatorRead)
async def update_operator(operator_id: int, data: OperatorUpdate, session: AsyncSession = Depends(get_session)):
    return await operators_dao.update_operator(session, operator_id, data=data)
    

# @router.get("/{operator_id}", response_model=OperatorRead)
# async def get_operator_by_id(operator_id: int, session: AsyncSession = Depends(get_session)):
#     q = await get_operator_by_id(session, operator_id)
#     if not q:
#         raise HTTPException(status_code=404, detail="Operator not found")
#     return q

# @router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_question(question_id: int, session: AsyncSession = Depends(get_session)):
#     ok = await delete_question(session, question_id)
#     if not ok:
#         raise HTTPException(status_code=404, detail="Question not found")
    
