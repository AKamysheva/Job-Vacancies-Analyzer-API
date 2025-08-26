from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.vacancy_service import parse_and_save
from app.db.database import get_db

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/parse_vacancies")
async def parse_vacancies(
    query: str = "Python", per_page: int = 100, db: AsyncSession = Depends(get_db)
):
    saved = await parse_and_save(query, per_page, db)
    return {"saved_vacancies": len(saved), "vacancies": saved}
