import typer
import asyncio
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import init_models, get_session, engine, Base
from app.exceptions.exceptions import DuplicatedEntryError
from app.repository.service import UsersRepository
from app.schemas.models import UserSchema, UserSchemaResponse

app = FastAPI()
cli = typer.Typer()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/")
async def get_users(session: AsyncSession = Depends(get_session)):
    repository = UsersRepository(session=session)
    users = await repository.get_users()
    return [UserSchemaResponse(name=c.name, id=c.id) for c in users]


@app.post("/users/")
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    repository = UsersRepository(session=session)
    user = await repository.add_user(name=user.name)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("User exist")

