from sqlalchemy.ext.asyncio import AsyncSession


class LimitedSession:
    def __init__(self, session: AsyncSession) -> None:
        self.get = session.get
        self.execute = session.execute
        self.flush = session.flush
        self.refresh = session.refresh
        self.add = session.add
        self.delete = session.delete
        self.scalar = session.scalar
        self.scalars = session.scalars
