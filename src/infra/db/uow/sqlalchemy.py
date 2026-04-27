from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infra.db.session import LimitedSession

from .base import UoWBase, UoWNotStartedError


class SqlAlchemyUoWBase(UoWBase, ABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._factory = session_factory
        self._session: AsyncSession | None = None

    @abstractmethod
    async def _init(self, session: LimitedSession) -> None: ...

    async def __aenter__(self) -> Self:
        if self._session is not None:
            raise RuntimeError("Unit of work is already active")

        self._session = self._factory()
        await self._init(LimitedSession(self._session))
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if self._session is None:
            raise UoWNotStartedError()

        if exc_type or self._session.in_transaction():
            await self._session.rollback()

        await self._session.aclose()
        self._session = None

    async def rollback(self) -> None:
        if self._session is None:
            raise UoWNotStartedError()
        await self._session.rollback()

    async def commit(self) -> None:
        if self._session is None:
            raise UoWNotStartedError()
        await self._session.commit()
