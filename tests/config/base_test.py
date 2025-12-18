from tests.services.books.api_books import BooksAPI


class BaseTest:

    def setup_method(self):
        self.api_books = BooksAPI()
