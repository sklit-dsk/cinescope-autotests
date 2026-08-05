import pytest
import allure

from pytest_check import check
from models.movie_models import (
    ResponseMovie,
    ResponseGetMovie,
    MovieModel,
    MovieParamsModel,
)
from utils.data_generator import DataGenerator
from entities.user import User
from clients.api_manager import ApiManager
from db_requester.db_helpers import DBHelper

@allure.epic("Тестирование фильмов")
@allure.feature("Тестирование операций с фильмами")
@allure.label("qa_name", "Danila")
class TestMovies:

    @allure.story("Корректность получения фильмов без параметров в запросе")
    @allure.description("""
        Этот тест проверяет корректность получения фильма без передачи параметров в запросе
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильмов без параметров.")
    @pytest.mark.api
    def test_get_movies_without_params(self, api_manager: ApiManager) -> None:
        with allure.step("Получение фильмов"):
            ResponseGetMovie(**api_manager.movies_api.get_movies().json())

    @allure.story("Корректность создания фильма.")
    @allure.description("""
            Этот тест проверяет корректность создания фильма.
            """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания фильма")
    @pytest.mark.api
    def test_create_movie(self, created_movie: ResponseMovie) -> None:
        with allure.step("Создание фильма и валидация ответа сервера"):
            ResponseMovie(**created_movie.model_dump())

    @allure.story("Корректность получения фильмов по id")
    @allure.description("""
        Этот тест проверяет корректность получения фильма по id
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильмов по id")
    @pytest.mark.api
    def test_get_movie_by_id(
        self, super_admin: User, created_movie: ResponseMovie
    ) -> None:
        with allure.step("Получение фильма по id"):
            ResponseMovie(
                **super_admin.api.movies_api.get_movie_by_id(
                    movie_id=created_movie.id, expected_status=200
                ).json()
            )

    @allure.story("Корректность удаления фильма")
    @allure.description("""
        Этот тест проверяет корректность удаления фильма.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма")
    @pytest.mark.api
    def test_delete_movie(
        self, super_admin: User, created_movie: ResponseMovie
    ) -> None:
        with allure.step("Создание и валидация созданного фильма"):
            response = ResponseMovie(**created_movie.model_dump())
        with allure.step("Удаление фильма"):
            response_delete_movie = ResponseMovie(
                **super_admin.api.movies_api.delete_movie_by_id(
                    movie_id=response.id
                ).json()
            )
        with allure.step("Попытка получить удаленный фильм"):
            super_admin.api.movies_api.get_movie_by_id(
                movie_id=response_delete_movie.id, expected_status=404
            )

    @allure.story("Корректность обновления фильма")
    @allure.description("""
        Этот тест проверяет корректность обновления фильма.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест обновления фильма")
    @pytest.mark.api
    def test_patch_movie(
        self,
        super_admin: User,
        created_movie: ResponseMovie,
        movie_data: MovieModel,
    ) -> None:
        with allure.step("Валидация созданного фильма"):
            response = ResponseMovie(**created_movie.model_dump())
        with allure.step("Создание и валидация данных для обновления фильма"):
            new_movie_data = movie_data.model_copy()
            new_movie_data.name = DataGenerator.generate_movie_name()
            new_movie_data.price = DataGenerator.generate_min_price()
        with allure.step(
            "Отправка patch запроса с новыми данными для частичного изменения"
        ):
            response_patch_movie = ResponseMovie(
                **super_admin.api.movies_api.patch_movie_by_id(
                    movie_id=response.id, data=new_movie_data, expected_status=200
                ).json()
            )

        with allure.step("Получение изменненого фильма после patch"):
            response_get_patched_movie = ResponseMovie(
                **super_admin.api.movies_api.get_movie_by_id(
                    movie_id=response_patch_movie.id, expected_status=200
                ).json()
            )
        with check:
            check.equal(response_get_patched_movie.name, response_patch_movie.name)
            check.equal(response_get_patched_movie.price, response_patch_movie.price)

    @allure.story(
        "Корректность получения фильмов с параметрами в запросе и параметризацией"
    )
    @allure.description("""
        Этот тест проверяет корректность получения фильмов с передачей параметров в запросе.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильмов с параметрами через parametrize")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "price,location,genreId",
        [
            ((500, 600), "SPB", "8"),
            ((600, 700), "MSK", "9"),
            ((700, 1000), "SPB", "10"),
        ],
        ids=["SPB_test_1", "MSK_test", "SPB_test_2"],
    )
    def test_movies_with_parametrize_params(
        self,
        price: tuple[int, int],
        location: str,
        genreId: int,
        api_manager: ApiManager,
        movie_params: MovieParamsModel,
    ) -> None:
        with allure.step("Назначение новых параметров"):
            movie_params.minPrice = price[0]
            movie_params.maxPrice = price[1]
            movie_params.locations = location
            movie_params.genreId = genreId

        with allure.step("Получение фильмов соответствющих параметрам"):
            ResponseGetMovie(
                **api_manager.movies_api.get_movies(params=movie_params).json()
            )

    @allure.story("Корректность создания и удаления фильма в БД")
    @allure.description("""
        Этот тест проверяет корректность создания и удаления фильма с проверкой в базе данных.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания и удаления фильма с проверкой БД")
    @pytest.mark.api
    @pytest.mark.db
    @pytest.mark.flaky(reruns=3)
    def test_create_and_delete_movie_and_check_db(
        self, super_admin: User, movie_data: MovieModel, db_helper: DBHelper
    ):
        with allure.step("Попытка получить фильм из бд по имени"):
            assert db_helper.get_movie_by_name(movie_data.name) is None

        with allure.step("создание фильма по средствам API"):
            response = ResponseMovie(
                **super_admin.api.movies_api.create_movie(movie_data).json()
            )

        with allure.step("Получение созданного фильма из бд по id"):
            assert db_helper.get_movie_by_id(response.id) is not None

        with allure.step("Удаленеие фильма по средствам API"):
            response_deleted_movie = ResponseMovie(
                **super_admin.api.movies_api.delete_movie_by_id(response.id).json()
            )

        with allure.step("Проверка что фильм удален из бд."):
            assert db_helper.get_movie_by_id(response_deleted_movie.id) is None
