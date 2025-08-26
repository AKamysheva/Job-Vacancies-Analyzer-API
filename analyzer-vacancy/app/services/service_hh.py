from httpx import AsyncClient

async def get_vacancies(query: str = 'Python', per_page: int = 100):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': query, 'per_page': per_page}
    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()['items']
