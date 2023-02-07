from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Users


class UsersRepository:
    model = Users

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self):
        smtp = select(self.model)
        result = await self.session.execute(smtp)
        return result.scalars().all()

    async def check_user(self, name: str):
        smtp = (select(self.model.id, self.model.name).where(self.model.c.name == name))
        result = await self.session.execute(smtp)

    async def add_user(self, name: str):
        stmt = insert(self.model).values(name=name)
        result = await self.session.execute(stmt)
        return result


