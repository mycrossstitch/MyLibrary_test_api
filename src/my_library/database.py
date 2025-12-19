from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path


# 1. Настройка URL для SQLite (асинхронный драйвер aiosqlite)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "library.db"

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# 2. Создание движка (Engine)
engine = create_async_engine(DATABASE_URL)

# 3. Фабрика сессий (Session Factory)
new_session = async_sessionmaker(engine, expire_on_commit=False)


# 4. Базовый класс моделей
class Model(MappedAsDataclass, DeclarativeBase):
    pass


# Наша зависимость (Ассистент)
async def get_db():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
