import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

class MovieModel(BaseModel):
    name: str
    imageUrl: str
    price: int
    description: str
    location: str
    published: bool
    genreId: int

    model_config = ConfigDict(extra="forbid")

class ReviewsModel(BaseModel):
    userId: str
    hidden: bool
    text: str
    rating: int
    createdAt: str = Field(description="Дата и время создания отзыва в формате ISO 8601")

class GenreModel(BaseModel):
    name: str

class ResponseMovie(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: str
    location: str
    published: bool
    rating: float
    genreId: int
    createdAt: str = Field(description="Дата и время создания фильма в формате ISO 8601")
    reviews: Optional[list[ReviewsModel]] = None
    genre: GenreModel

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

class ResponseGetMovie(BaseModel):
    movies: list[ResponseMovie]
    count: int
    page: int
    pageSize: int
    pageCount: int


class MovieParamsModel(BaseModel):
    minPrice: float
    maxPrice: float
    locations: str
    published: bool
    genreId: int
    createdAt: str
