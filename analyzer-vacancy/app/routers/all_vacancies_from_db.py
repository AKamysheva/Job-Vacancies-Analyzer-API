from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.vacancy import VacancyOut
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import Vacancy
from typing import List


router = APIRouter(prefix='/all_vacancies_from_db', tags=['Vacancies'])

@router.get('/', response_model=List[VacancyOut])
async def get_all_vacancies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vacancy))
    vacancies = result.scalars().all()
    return vacancies