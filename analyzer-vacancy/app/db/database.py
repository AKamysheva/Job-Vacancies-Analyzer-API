from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings


engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

async def create_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {'ok': True}


