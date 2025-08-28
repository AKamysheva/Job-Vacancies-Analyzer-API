from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import (
    vacancies,
    parser,
    all_vacancies_from_db,
    delete_vacancy,
    export_vacancies,
)
from app.tasks import scheduler, start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(title="Analyzer's vacancy", lifespan=lifespan)

app.include_router(parser.router)
app.include_router(all_vacancies_from_db.router)
app.include_router(vacancies.router)
app.include_router(export_vacancies.router)
app.include_router(delete_vacancy.router)


@app.get("/")
async def root():
    return {"message": "ok"}
