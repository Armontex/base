from typing import Any

from sqlalchemy.orm import DeclarativeBase

from src.infra.db.session import LimitedSession


class BaseRepository[T: DeclarativeBase]:
    def __init__(self, model: type[T], session: LimitedSession) -> None:
        self._session = session
        self._model = model

    async def _create(self, **kwargs: Any) -> T:
        instance = self._model(**kwargs)
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def _get_by_id(self, id: Any) -> T | None:
        return await self._session.get(self._model, id)

    async def _update(self, instance: T, **fields: Any) -> None:
        for field_name, value in fields.items():
            if not hasattr(instance, field_name):
                raise AttributeError(
                    f"{type(instance).__name__} has no field '{field_name}'"
                )
            setattr(instance, field_name, value)
        await self._session.flush()

    async def _delete(self, instance: T) -> None:
        await self._session.delete(instance)
