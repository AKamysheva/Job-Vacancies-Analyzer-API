from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Vacancy
from app.db.database import get_db


router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.delete("/delete_vacancy_by_id/{vacancy_id}/")
async def delete_vacancy_from_db(vacancy_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id))
    vacancy = result.scalar_one_or_none()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    await db.delete(vacancy)
    await db.commit()
    return {"detail": "Vacancy with id={vacancy_id} deleted successfully"}
