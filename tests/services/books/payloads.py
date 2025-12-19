from faker import Faker

fake = Faker()


class Payloads:

    def create_book(self) -> dict:
        return {
            "title": fake.sentence(nb_words=3),
            "author": fake.name(),
            "year": fake.random_int(1900, 2024),
            "pages": fake.random_int(1, 1500),
            "is_read": fake.boolean(),
        }

    def create_books_bulk(self, count: int = 3):
        return [
            {
                "title": fake.sentence(nb_words=3),
                "author": fake.name(),
                "year": fake.random_int(1900, 2024),
                "pages": fake.random_int(1, 1500),
                "is_read": False,
            }
            for _ in range(count)
        ]
