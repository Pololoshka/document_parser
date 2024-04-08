from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )
