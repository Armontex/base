from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.networks import PostgresDsn


class DbSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    host: str = "postgres"
    alembic_host: str = "127.0.0.1"
    port: int = 5432
    name: str = Field(default="postgres", min_length=1)
    user: str = Field(default="postgres", min_length=1)
    password: str = Field(default="postgres", min_length=1)
    echo: bool = False
    sync_driver: str = Field(default="psycopg2", init=False)
    async_driver: str = Field(default="asyncpg", init=False)

    @computed_field
    @property
    def url_async(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.async_driver}",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.name,
            )
        )

    @computed_field
    @property
    def url_sync(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.sync_driver}",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.name,
            )
        )

    @computed_field
    @property
    def alembic_url_sync(self) -> str:
        host = self.alembic_host or self.host
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.sync_driver}",
                host=host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.name,
            )
        )
