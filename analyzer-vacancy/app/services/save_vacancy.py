from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Vacancy


async def save_vacancy(db: AsyncSession, vacancy: dict) -> Vacancy:
    if vacancy.get("archived"):
        return None

    hh_id = vacancy.get("hh_id")
    if not hh_id:
        return None

    vacancy_exists = await db.execute(select(Vacancy).where(Vacancy.hh_id == hh_id))
    if vacancy_exists.scalar_one_or_none():
        return None

    db_vacancy = Vacancy(**vacancy)
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy
