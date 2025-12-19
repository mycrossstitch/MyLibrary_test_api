from pydantic import BaseModel, ConfigDict, Field


# 1. Базовый класс (общие поля)
class SBookBase(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(gt=10)
    is_read: bool = False


# 2. Класс для создания (ничего не добавляет, просто копирует базу. Валидация: pages должно быть больше 10)
class SBookAdd(SBookBase):
    pass


# 3. Класс для чтения (добавляет id)
class SBook(SBookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
