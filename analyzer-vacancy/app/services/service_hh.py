import asyncio
from httpx import AsyncClient


# async def get_vacancies(query: str = 'Python', per_page: int = 100):
#     url = 'https://api.hh.ru/vacancies'
#     params = {'text': query, 'per_page': per_page}
#     async with AsyncClient() as client:
#         response = await client.get(url, params=params)
#         response.raise_for_status()
#         return response.json()['items']


class HHCollectorVacancies:
    def __init__(self, query: str = "Python", per_page: int = 100):
        self.query = query
        self.per_page = per_page
        self.hosts = [
            "hh.ru",
            "hh1.az",
            "hh.uz",
            "hh.kz",
            "headhunter.ge",
            "headhunter.kg",
            "rabota.by",
        ]

    async def collect_vacanсies_by_host(self, client, host):
        url = "https://api.hh.ru/vacancies"
        params = {"text": self.query, "per_page": self.per_page, "host": host}
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()["items"]

    async def get_vacancies(self):
        tasks = []
        async with AsyncClient() as client:
            for host in self.hosts:
                task = asyncio.create_task(self.collect_vacanсies_by_host(client, host))
                tasks.append(task)

            result = await asyncio.gather(*tasks)
        return [v for host_lst in result for v in host_lst]
