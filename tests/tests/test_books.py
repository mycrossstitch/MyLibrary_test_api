import allure
import pytest

from tests.config.base_test import BaseTest


@allure.epic("Books")
@allure.feature("Book")
class TestBooks(BaseTest):

    @pytest.mark.regression
    @allure.title("Create new book")
    def test_create_book(self):
        book = self.api_books.create_book()
        self.api_books.get_book_by_id(book.id)
        self.api_books.delete_book_by_id(book.id)

    @pytest.mark.regression
    @allure.title("Update book - full update")
    def test_update_book_full(self):
        book = self.api_books.create_book()
        self.api_books.update_book_full(book.id)
        self.api_books.delete_book_by_id(book.id)

    @pytest.mark.regression
    @allure.title("Create books in bulk")
    def test_create_books_bulk(self):
        books = self.api_books.create_books_bulk()

        for book in books:
            self.api_books.get_book_by_id(book.id)
            self.api_books.delete_book_by_id(book.id)


@allure.epic("Books")
@allure.feature("Book - negative")
@pytest.mark.negative
class TestBooksNegative(BaseTest):

    @pytest.mark.regression
    def test_create_book_empty_body(self):
        self.api_books.create_book_empty_body()

    @pytest.mark.regression
    def test_create_book_invalid_types(self):
        self.api_books.create_book_invalid_types()

    @pytest.mark.regression
    def test_get_book_invalid_id(self):
        self.api_books.get_book_by_invalid_id()

    @pytest.mark.regression
    def test_update_book_invalid_id(self):
        self.api_books.update_book_invalid_id()

    @pytest.mark.regression
    def test_update_book_incomplete_body(self):
        book = self.api_books.create_book()
        self.api_books.update_book_incomplete_body(book.id)
        self.api_books.delete_book_by_id(book.id)

    @pytest.mark.regression
    def test_delete_book_twice(self):
        book = self.api_books.create_book()
        self.api_books.delete_book_twice(book.id)

    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="API allows empty bulk payload, validation is missing"
    )  # тест провален, ошибка в API - при пустом списке код 201
    def test_create_books_bulk_empty(self):
        self.api_books.create_books_bulk_empty()

    @pytest.mark.regression
    def test_create_books_bulk_invalid_item(self):
        self.api_books.create_books_bulk_with_invalid_item()
