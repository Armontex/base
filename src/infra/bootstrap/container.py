from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.infra.config import Settings


class Container(containers.DeclarativeContainer):
    settings = providers.Dependency(instance_of=Settings)
    session_factory = providers.Dependency(instance_of=async_sessionmaker)
