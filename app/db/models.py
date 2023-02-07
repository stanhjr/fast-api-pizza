from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from app.db.base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
