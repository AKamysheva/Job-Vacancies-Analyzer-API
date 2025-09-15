import pytest
from app.services.vacancy_service import get_vacancies_from_db, parse_and_save
from app.services.service_hh import HHCollectorVacancies
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_get_vacancies_from_db(async_db: AsyncSession):
    result = await get_vacancies_from_db(async_db)
    assert len(result) == 2
    assert result[0].hh_id == 123456


@pytest.mark.asyncio
async def test_parse_and_save(async_db, fake_vacancies):
    with (
        patch(
            "app.services.vacancy_service.HHCollectorVacancies.get_vacancies",
            new_callable=AsyncMock,
        ) as mock_get_vacancies,
        patch(
            "app.services.vacancy_service.delete_archived_vacancies",
            new_callable=AsyncMock,
        ) as mock_delete_archived_vacancies,
    ):
        mock_get_vacancies.return_value = fake_vacancies
        mock_delete_archived_vacancies.return_value = None
        saved = await parse_and_save("Python", 1, async_db)

    mock_get_vacancies.assert_awaited_once()
    mock_delete_archived_vacancies.assert_awaited_once()

    assert len(saved) == 1
    assert saved[0].title == "Python Developer"


@pytest.fixture
def fake_response():
    return [{"id": "1"}, {"id": "2"}]


@pytest.fixture
def collector():
    return HHCollectorVacancies()


@pytest.fixture
def mock_method():
    with patch.object(
        HHCollectorVacancies, "collect_vacanсies_by_host", new_callable=AsyncMock
    ) as mock:
        yield mock


def assert_vacancies_result(result, expected_count):
    assert len(result) == expected_count
    assert all("id" in v for v in result)


@pytest.mark.asyncio
async def test_get_vacancies_from_api(collector, mock_method, fake_response):
    mock_method.return_value = fake_response
    result = await collector.get_vacancies()
    assert_vacancies_result(result, len(collector.hosts) * 2)


@pytest.mark.asyncio
async def test_get_vacancies_from_api_with_host_error(
    collector, mock_method, fake_response
):
    async def side_effect(client, host):
        if host == "hh.uz":
            raise Exception("Host error")
        return fake_response

    mock_method.side_effect = side_effect
    result = await collector.get_vacancies()
    assert_vacancies_result(result, (len(collector.hosts) - 1) * 2)
