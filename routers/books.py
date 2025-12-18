from fastapi import APIRouter, HTTPException, status
from typing import Annotated, List
from database import SessionDep
from repository.books import BookRepository
from schemas.books import SBook, SBookAdd

router = APIRouter(prefix="/books", tags=["Книги"])


@router.post(
    "",
    response_model=SBook,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить одну книгу",
)
async def create_book(
    book: SBookAdd,
    session: SessionDep,
):

    book_model = await BookRepository.add_one(book, session)
    return book_model


@router.post(
    "/bulk",
    response_model=List[SBook],
    status_code=status.HTTP_201_CREATED,
    summary="Добавить несколько книг",
)
async def create_books_bulk(
    books: List[SBookAdd],
    session: SessionDep,
):
    created_books = []
    for book in books:
        book_model = await BookRepository.add_one(book, session)
        created_books.append(book_model)
    return created_books


@router.get("", status_code=status.HTTP_200_OK, summary="Получить все книги")
async def get_book(session: SessionDep):

    books = await BookRepository.find_all(session)
    return books


@router.get(
    "/is_read",
    status_code=status.HTTP_200_OK,
    summary="Получить книги по статусу прочтения",
)
async def get_books_by_read_status(
    session: SessionDep, is_read: bool = False
):  # По умолчанию False (непрочитанные)
    books = await BookRepository.find_by_is_read(is_read, session)
    return books


@router.get(
    "/search",
    response_model=List[SBook],
    status_code=status.HTTP_200_OK,
    summary="Поиск книг по параметрам",
)
async def search_books(
    session: SessionDep,
    author: str | None = None,
    title: str | None = None,
    year: int | None = None,
):
    """Поиск книг по параметрам"""
    books = await BookRepository.search_books(
        session=session, author=author, title=title, year=year
    )
    return books


@router.get("/{id}", status_code=status.HTTP_200_OK, summary="Получить книгу по ID")
async def get_book_by_id(id: int, session: SessionDep):

    book = await BookRepository.get_one(id, session)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Книга с ID {id} не найдена"
        )
    return book


@router.put(
    "/{id}",
    response_model=SBook,
    status_code=status.HTTP_200_OK,
    summary="Обновить книгу по ID",
)
async def update_book(
    id: int,
    book_data: SBookAdd,
    session: SessionDep,
):
    """Полностью заменяет пользователя с указанным ID"""
    # Проверяем существование книги
    existing_book = await BookRepository.get_one(id, session)
    if existing_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Книга с ID {id} не найдена"
        )
    updated_book = await BookRepository.update_one(id, book_data, session)
    return updated_book


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить книгу по ID"
)
async def delete_book(id: int, session: SessionDep):
    delete_book = await BookRepository.get_one(id, session)
    if delete_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Книга с ID {id} не найдена"
        )
    await BookRepository.delete_one(id, session)
