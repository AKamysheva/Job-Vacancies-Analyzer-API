import re
from fastapi import Depends
from app.db.database import get_db
from app.db.models import Vacancy
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.service_hh import HHCollectorVacancies
from app.services.save_vacancy import save_vacancy
from app.services.delete import delete_archived_vacancies
from dateutil.parser import parse


def clean_description(item):
    text = (
        item.get("description")
        or item.get("snippet", {}).get("requirement")
        or item.get("snippet", {}).get("responsibility")
        or "Описание отсутствует"
    )
    text = re.sub(r"</?highlighttext>", "", text)
    return text


def get_skills(item):
    skills = [skill["name"] for skill in item.get("key_skills", [])]
    if not skills:
        skills = [role["name"] for role in item.get("professional_roles", [])]

    return skills


def filter_vacancies(data: list, keyword: str):
    filtered = []
    for item in data:
        lst_work_format = item.get("work_format", [])
        if not lst_work_format or not lst_work_format[0].get(
            "name", ""
        ).lower().startswith("удал"):
            continue

        requirement = item.get("snippet", {}).get("requirement") or ""
        if (
            keyword.lower() not in item.get("name", "").lower()
            or keyword.lower() not in requirement.lower()
        ):
            continue

        filtered.append(
            {
                "hh_id": item["id"],
                "title": item["name"],
                "skills": get_skills(item),
                "description": clean_description(item),
                "published_at": parse(item["published_at"]).date(),
                "work_format": (
                    lst_work_format[0].get("name", "") if lst_work_format else ""
                ),
                "url": item.get("url", ""),
            }
        )

    return filtered


async def parse_and_save(query: str, per_page: int, db: AsyncSession):
    collector = HHCollectorVacancies(query=query, per_page=per_page)
    raw_vacancies = await collector.get_vacancies()
    vacancies = filter_vacancies(raw_vacancies, query)

    await delete_archived_vacancies(db)

    saved_vacancies = []

    for vac in vacancies:
        saved = await save_vacancy(db, vac)
        if saved:
            saved_vacancies.append(saved)

    return saved_vacancies


async def get_vacancies_from_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vacancy))
    vacancies = result.scalars().all()
    return vacancies
