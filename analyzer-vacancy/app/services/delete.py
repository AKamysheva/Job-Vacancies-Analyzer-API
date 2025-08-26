import asyncio
import httpx

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Vacancy


async def delete_archived_vacancies(db: AsyncSession):
    result = await db.execute(select(Vacancy.hh_id))
    hh_ids = result.scalars().all()

    semaphore = asyncio.Semaphore(10)

    async def check_and_delete(hh_id: str):
        async with semaphore:
            url_hh = f"https://api.hh.ru/vacancies/{hh_id}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url_hh)

            if response.status_code == 404:
                return hh_id
            if response.status_code != 200:
                return None

            data = response.json()
            vacancy_type = data.get("type", {}).get("id", "").lower()
            if vacancy_type != "open":
                return hh_id

    archived_ids = await asyncio.gather(*(check_and_delete(hh_id) for hh_id in hh_ids))
    archived_ids = [i for i in archived_ids if i]
    if archived_ids:
        await db.execute(delete(Vacancy).where(Vacancy.hh_id.in_(archived_ids)))
        await db.commit()
