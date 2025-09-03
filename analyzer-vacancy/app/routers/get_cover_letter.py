from fastapi import APIRouter
from app.services.cover_letter import generate_cover_letter

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/generate_cover_letter/{vacancy_id}")
async def generate_cover_letter_to_resume(vacancy_id: int):
    result = await generate_cover_letter(vacancy_id)
    return result
