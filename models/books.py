from sqlalchemy.orm import Mapped, mapped_column
from database import Model


class BooksModel(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True, init=False
    )  # Первичный ключ (Primary Key)
    title: Mapped[str]  # Название книги (не может быть пустым)
    author: Mapped[str]  # Автор книги (не может быть пустым)
    year: Mapped[int | None]  # Год издания
    pages: Mapped[int | None]  # Количество страниц
    is_read: Mapped[bool] = mapped_column(
        default=False
    )  # Прочитана ли книга (по умолчанию False)
