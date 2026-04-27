from abc import ABC, abstractmethod


class UoWNotStartedError(RuntimeError):
    message = "Unit of work is not active. Use 'async with uow:' context manager."

    def __init__(self) -> None:
        super().__init__(self.message)


class UoWBase(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

