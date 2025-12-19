from typing import List

from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_library.models.books import BooksModel
from src.my_library.schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        # 1. Превращаем данные из Pydantic в словарь
        book_dict = data.model_dump()

        # 2. Создаем объект модели
        book = BooksModel(**book_dict)

        # 3. Добавляем и сохраняем
        session.add(book)
        await session.commit()
        await session.refresh(book)

        # 4. Возвращаем созданный объект
        return book

    @classmethod
    async def find_all(cls, session: AsyncSession):
        # 1. Готовим запрос
        query = select(BooksModel)

        # 2. Выполняем
        result = await session.execute(query)

        # 3. Возвращаем список объектов
        books_models = result.scalars().all()
        return books_models

    @classmethod
    async def get_one(cls, book_id: int, session: AsyncSession):
        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)
        book = result.scalars().one_or_none()
        return book

    @classmethod
    async def update_one(
        cls, book_id: int, book_data: SBookAdd, session: AsyncSession
    ) -> BooksModel:
        # 1. Превращаем данные из Pydantic в словарь
        book_dict = book_data.model_dump()

        # 2. Создаем запрос на обновление
        stmt = (
            update(BooksModel)
            .where(BooksModel.id == book_id)
            .values(**book_dict)
            .returning(BooksModel)
        )

        # 3. Выполняем запрос
        result = await session.execute(stmt)
        await session.commit()

        # 4. Возвращаем обновленный объект
        updated_book = result.scalar_one()
        await session.refresh(updated_book)
        return updated_book

    @classmethod
    async def delete_one(cls, book_id: int, session: AsyncSession):
        stmt = delete(BooksModel).where(BooksModel.id == book_id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def search_books(
        cls,
        session: AsyncSession,
        author: str | None = None,
        title: str | None = None,
        year: int | None = None,
    ) -> List[BooksModel]:
        """Поиск книг по параметрам"""
        query = select(BooksModel)
        # Собираем условия
        conditions = []
        if author:
            conditions.append(func.lower(BooksModel.author).contains(author.lower()))
        if title:
            conditions.append(func.lower(BooksModel.title).contains(title.lower()))
        if year is not None:
            conditions.append(BooksModel.year == year)
        # Применяем условия, если они есть
        if conditions:
            query = query.where(and_(*conditions))
        # Выполняем запрос
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_by_is_read(cls, is_read: bool, session: AsyncSession):
        # 1. Готовим запрос
        query = select(BooksModel).where(BooksModel.is_read == is_read)
        # 2. Выполняем
        result = await session.execute(query)
        # 3. Возвращаем список объектов
        books_models = result.scalars().all()
        return books_models
