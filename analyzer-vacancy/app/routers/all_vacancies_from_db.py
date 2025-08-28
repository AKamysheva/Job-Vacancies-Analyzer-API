from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.vacancy import VacancyOut
from app.services.vacancy_service import get_vacancies_from_db
from app.db.database import get_db
from typing import List


router = APIRouter(prefix="/all_vacancies_from_db", tags=["Vacancies"])


@router.get("/", response_model=List[VacancyOut])
async def get_all_vacancies(db: AsyncSession = Depends(get_db)):
    vacancies = await get_vacancies_from_db(db)
    return vacancies
