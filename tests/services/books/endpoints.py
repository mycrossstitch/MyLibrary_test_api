import os

HOST = os.getenv(
    "API_HOST", "http://127.0.0.1:8000"
)  # if os.environ["STAGE"] == "qa" else ""


class Endpoints:

    create_book = f"{HOST}/books"
    get_books_list = f"{HOST}/books"
    get_book_by_id = lambda self, book_id: f"{HOST}/books/{book_id}"
    delete_book_by_id = lambda self, book_id: f"{HOST}/books/{book_id}"
    update_book_by_id = lambda self, book_id: f"{HOST}/books/{book_id}"
    create_books_bulk = f"{HOST}/books/bulk"
