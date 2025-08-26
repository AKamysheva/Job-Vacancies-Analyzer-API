from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    USER_DB: str
    PASSWORD_DB: str
    NAME_DB: str
    HOST_DB: str
    PORT_DB: int

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.USER_DB}:{self.PASSWORD_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}"

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
