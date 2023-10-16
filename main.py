from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL)

# Создание асинхронной сессии
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Создание базовой декларативной модели
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Описание модели таблицы "User"
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


app = FastAPI()


class UserBase(BaseModel):
    id: int
    name: str
    email: str


# Pydantic модель для входных данных
class UserCreate(BaseModel):
    name: str
    email: str


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    pass


@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    async with async_session() as session:
        db_user = User(name=user.name, email=user.email)
        session.add(db_user)
        try:
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Cannot create user")


@app.get("/users/", response_model=List[UserBase])
async def fetch_users():
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users


@app.get("/users/{user_id}/", response_model=UserCreate)
async def read_user(user_id: int):
    async with async_session() as session:
        stmt = select(User).filter(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@app.put("/users/{user_id}/", response_model=UserCreate)
async def update_user(user_id: int, user: UserCreate):
    async with async_session() as session:
        db_user = session.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.name = user.name
        db_user.email = user.email
        await session.commit()
        await session.refresh(db_user)
        return db_user


@app.delete("/users/{user_id}/", response_model=UserCreate)
async def delete_user(user_id: int):
    async with async_session() as session:
        db_user = session.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(db_user)
        await session.commit()
        return db_user


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
    )
