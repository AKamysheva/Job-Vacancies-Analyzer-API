import csv

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from io import StringIO, BytesIO
from app.db.database import get_db
from app.db.models import Vacancy
from app.services.vacancy_service import get_vacancies_from_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/export_vacancies")
async def export_vacancies_in_file(db: AsyncSession = Depends(get_db)):
    vacancies = await get_vacancies_from_db(db)

    fieldnames = Vacancy.__table__.columns.keys()

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for vac in vacancies:
        writer.writerow({k: getattr(vac, k) for k in fieldnames})

    bytes_output = BytesIO(output.getvalue().encode("utf-8-sig"))
    bytes_output.seek(0)

    return StreamingResponse(
        bytes_output,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=vacancies.csv"},
    )
