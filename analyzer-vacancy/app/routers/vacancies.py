from fastapi import APIRouter, Query, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.vacancy import VacancyOut
from app.db.database import get_db
from app.db.models import Vacancy
from typing import List


router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/search_db_by_keyword", response_model=List[VacancyOut])
async def read_vacancies_by_keyword(
    query: str = Query(None), db: AsyncSession = Depends(get_db)
):
    stmt = select(Vacancy)
    if query:
        stmt = stmt.where(Vacancy.title.ilike(f"%{query}%"))
    result = await db.execute(stmt)
    return result.scalars().all()
