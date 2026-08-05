import pytest
import allure
from entities.user import User
from utils.data_generator import DataGenerator
from models.movie_models import (
    MovieModel,
    ResponseMovie,
    MovieParamsModel,
)
from collections.abc import Generator


@pytest.fixture(scope="function")
def movie_params() -> MovieParamsModel:
    with allure.step("Генерация параметров для получения фильмов"):
        min_price = DataGenerator.generate_min_price()
        return MovieParamsModel(
            minPrice=min_price,
            maxPrice=DataGenerator.generate_max_price(min_price),
            locations=DataGenerator.generate_location(),
            published=DataGenerator.generate_published(),
            genreId=DataGenerator.generate_genre_id(),
            createdAt=DataGenerator.generate_created_at(),
        )


@pytest.fixture(scope="function")
def bad_movie_params() -> MovieParamsModel:
    with allure.step("Генерация невалидных параметров для получения фильмов"):
        min_price = DataGenerator.generate_min_price()
        return MovieParamsModel(
            minPrice=min_price,
            maxPrice=DataGenerator.generate_max_price(min_price),
            locations=DataGenerator.generate_bad_location(),
            published=DataGenerator.generate_published(),
            genreId=DataGenerator.generate_genre_id(),
            createdAt=DataGenerator.generate_created_at(),
        )


@pytest.fixture(scope="function")
def movie_data() -> MovieModel:
    with allure.step("Генерация тестовых данных фильма"):
        return MovieModel(
            name=DataGenerator.generate_movie_name(),
            imageUrl=DataGenerator.generate_movie_image_url(),
            price=DataGenerator.generate_min_price(),
            description=DataGenerator.generate_movie_description(),
            location=DataGenerator.generate_location(),
            published=DataGenerator.generate_published(),
            genreId=DataGenerator.generate_genre_id(),
        )


@pytest.fixture(scope="function")
def created_movie(
    super_admin: User, movie_data: MovieModel
) -> Generator[ResponseMovie, None, None]:
    with allure.step("Создание фильма"):
        response = ResponseMovie(
            **super_admin.api.movies_api.create_movie(movie_data).json()
        )
    yield response
    with allure.step("Удаление фильма после теста"):
        response_delete_movie = super_admin.api.session.request(
            "DELETE",
            f"{super_admin.api.movies_api.base_url}/movies/{response.id}",
        )
        if response_delete_movie.status_code not in (200, 404):
            raise ValueError(
                f"Unexpected status code during cleanup: {response_delete_movie.status_code}"
            )
