from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Model
from routers.books import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- КОД ПРИ СТАРТЕ ---
    # Мы обращаемся к движку и просим создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("База данных готова к работе")

    yield  # Разделяет старт и выключение

    # --- КОД ПРИ ВЫКЛЮЧЕНИИ ---
    print("Выключение сервера")


# Передаем lifespan в приложение
app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
