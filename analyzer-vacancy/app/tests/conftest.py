import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.db.database import get_db
from app.db.models import Base, Vacancy
from sqlalchemy.pool import StaticPool
from datetime import date

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


testing_async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

client = TestClient(app)


@pytest.fixture
async def overrirde_get_db():
    async with testing_async_session() as session:
        yield session


app.dependency_overrides[get_db] = overrirde_get_db


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


@pytest.fixture
def fake_vacancies():
    return [
        {
            "id": 567894,
            "name": "Python Developer",
            "snippet": {"requirement": "Python Developer"},
            "skills": ["Skill1"],
            "description": "Python Developer",
            "published_at": "2025-09-10T12:00:00",
            "work_format": [{"name": "Удаленно"}],
            "url": "https://fake",
        },
        {
            "id": 67895,
            "name": "Java Developer",
            "snippet": {"requirement": "Java Developer"},
            "skills": ["Skill1"],
            "description": "Java Developer",
            "published_at": "2025-09-10T12:00:00",
            "work_format": [{"name": "офис"}],
            "url": "https://fake2",
        },
    ]


@pytest_asyncio.fixture
async def async_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with testing_async_session() as session:
        remote_vacancy = Vacancy(
            hh_id=123456,
            title="Test remote vacancy",
            description="Test description",
            skills=["Test skills"],
            published_at=date.today(),
            work_format="удаленно",
            url="https://test-remote",
        )

        remote_vacancy_2 = Vacancy(
            hh_id=567890,
            title="Test office vacancy",
            description="Office job description",
            skills=["Skill1", "Skill2"],
            published_at=date.today(),
            work_format="удаленно",
            url="https://test-office",
        )
        session.add_all([remote_vacancy, remote_vacancy_2])
        await session.commit()

        yield session

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
