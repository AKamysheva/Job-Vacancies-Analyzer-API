from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.database import async_session
from app.services.vacancy_service import parse_and_save

scheduler = AsyncIOScheduler()

async def load_vacancies_daily():
    async with async_session() as db:
        await parse_and_save(query="Python", per_page=100, db=db)

def start_scheduler():
    scheduler.add_job(load_vacancies_daily, 'cron', hour=9, minute=0)
    scheduler.start()