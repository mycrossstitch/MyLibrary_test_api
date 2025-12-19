import allure
import requests

from tests.config.headers import Headers
from tests.services.books.endpoints import Endpoints
from tests.services.books.payloads import Payloads
from tests.utils.helper import Helper
from src.my_library.schemas.books import SBook


class BooksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoint = Endpoints()
        self.headers = Headers()

    @allure.step("Create new book")
    def create_book(self):
        response = requests.post(
            url=self.endpoint.create_book,
            headers=self.headers.basic,
            json=self.payloads.create_book(),
        )
        assert response.status_code == 201, response.json()
        self.attach_response(response.json())
        model = SBook(**response.json())
        return model

    @allure.step("Get books by id")
    def get_book_by_id(self, id):
        response = requests.get(
            url=self.endpoint.get_book_by_id(id), headers=self.headers.basic
        )

        assert response.status_code == 200, response.json()
        self.attach_response(response.json())
        model = SBook(**response.json())
        return model

    @allure.step("Delete books by id")
    def delete_book_by_id(self, id):
        response = requests.delete(
            url=self.endpoint.delete_book_by_id(id), headers=self.headers.basic
        )

        assert response.status_code == 204, response.json()

    @allure.step("Update book by id (full update)")
    def update_book_full(self, book_id):
        payload = self.payloads.create_book()

        response = requests.put(
            url=self.endpoint.update_book_by_id(book_id),
            headers=self.headers.basic,
            json=payload,
        )

        assert response.status_code == 200, response.json()
        self.attach_response(response.json())
        book = SBook(**response.json())

        #  проверки контракта
        assert book.id == book_id
        assert book.title == payload["title"]
        assert book.author == payload["author"]
        assert book.year == payload["year"]
        assert book.pages == payload["pages"]
        assert book.is_read == payload["is_read"]

        return book

    @allure.step("Create books in bulk")
    def create_books_bulk(self, expected_count: int = 3):
        payload = self.payloads.create_books_bulk(expected_count)

        response = requests.post(
            url=self.endpoint.create_books_bulk,
            headers=self.headers.basic,
            json=payload,
        )

        assert response.status_code == 201, response.json()
        self.attach_response(response.json())

        books = [SBook(**item) for item in response.json()]

        assert len(books) == expected_count

        for book in books:
            assert book.id is not None

        return books

    # негативные тесты

    @allure.step("Create book with empty body - expect 422")
    def create_book_empty_body(self):
        response = requests.post(
            url=self.endpoint.create_book,
            headers=self.headers.basic,
            json={},
        )

        assert response.status_code == 422
        self.attach_response(response.json())

    @allure.step("Create book with invalid field types - expect 422")
    def create_book_invalid_types(self):
        payload = self.payloads.create_book()
        payload["title"] = 123

        response = requests.post(
            url=self.endpoint.create_book,
            headers=self.headers.basic,
            json=payload,
        )

        assert response.status_code == 422
        self.attach_response(response.json())

    @allure.step("Get book by non-existent id - expect 404")
    def get_book_by_invalid_id(self):
        response = requests.get(
            url=self.endpoint.get_book_by_id(999999),
            headers=self.headers.basic,
        )

        assert response.status_code == 404
        self.attach_response(response.json())

    @allure.step("Update non-existent book - expect 404")
    def update_book_invalid_id(self):
        response = requests.put(
            url=self.endpoint.update_book_by_id(999999),
            headers=self.headers.basic,
            json=self.payloads.create_book(),
        )

        assert response.status_code == 404
        self.attach_response(response.json())

    @allure.step("Update book with incomplete body - expect 422")
    def update_book_incomplete_body(self, book_id):
        response = requests.put(
            url=self.endpoint.update_book_by_id(book_id),
            headers=self.headers.basic,
            json={"title": "Only title"},
        )

        assert response.status_code == 422
        self.attach_response(response.json())

    @allure.step("Delete already deleted book - expect 404")
    def delete_book_twice(self, book_id):
        # first delete
        self.delete_book_by_id(book_id)

        # second delete
        response = requests.delete(
            url=self.endpoint.delete_book_by_id(book_id),
            headers=self.headers.basic,
        )

        assert response.status_code == 404
        self.attach_response(response.json())

    # тест провален, ошибка в API - при пустом списке код 201
    @allure.step("Create books in bulk with empty list - expect 422")
    def create_books_bulk_empty(self):
        response = requests.post(
            url=self.endpoint.create_books_bulk,
            headers=self.headers.basic,
            json=[],
        )

        assert response.status_code == 422
        self.attach_response(response.json())

    @allure.step("Create books in bulk with invalid item - expect 422")
    def create_books_bulk_with_invalid_item(self):
        payload = [
            self.payloads.create_book(),
            {"title": "Invalid only title"},
        ]

        response = requests.post(
            url=self.endpoint.create_books_bulk,
            headers=self.headers.basic,
            json=payload,
        )

        assert response.status_code == 422
        self.attach_response(response.json())
