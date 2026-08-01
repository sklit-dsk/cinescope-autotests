import pytest
import allure
from venv import logger
from models.movie_models import ResponseMovie, ResponseGetMovie, MovieModel
from utils.data_generator import DataGenerator
from entities.user import User


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
    def test_get_movies_without_params(self, api_manager) -> None:
        response = api_manager.movies_api.get_movies()
        response_data = response.json()
        ResponseGetMovie(**response_data)

    @allure.story("Корректность создания фильма.")
    @allure.description("""
            Этот тест проверяет корректность создания фильма.
            """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания фильма")
    @pytest.mark.api
    def test_create_movie(self, created_movie) -> None:
        response = created_movie.json()
        logger.info(response)
        ResponseMovie(**response)

    @allure.story("Корректность получения фильмов по id")
    @allure.description("""
        Этот тест проверяет корректность получения фильма по id
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильмов по id")
    @pytest.mark.api
    def test_get_movie_by_id(self, super_admin, created_movie) -> None:
        response_movie = super_admin.api.movies_api.get_movie_by_id(
            movie_id=created_movie.json()["id"], expected_status=200
        )
        logger.info(response_movie.json())
        ResponseMovie(**response_movie.json())

    @allure.story("Корректность удаления фильма")
    @allure.description("""
        Этот тест проверяет корректность удаления фильма.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма")
    @pytest.mark.api
    def test_delete_movie(self, super_admin, created_movie) -> None:
        response = created_movie.json()
        response_delete_movie = super_admin.api.movies_api.delete_movie_by_id(
            movie_id=response["id"]
        )
        super_admin.api.movies_api.get_movie_by_id(
            movie_id=response_delete_movie.json()["id"], expected_status=404
        )

    @allure.story("Корректность обновления фильма")
    @allure.description("""
        Этот тест проверяет корректность обновления фильма.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест обновления фильма")
    @pytest.mark.api
    def test_patch_movie(self, super_admin, created_movie, movie_data) -> None:
        response = created_movie.json()
        new_movie_data = movie_data.copy()
        new_movie_data["name"] = DataGenerator.generate_movie_name()
        new_movie_data["price"] = DataGenerator.generate_min_price()
        MovieModel(**new_movie_data)
        response_patch_movie = super_admin.api.movies_api.patch_movie_by_id(
            movie_id=response["id"], data=new_movie_data, expected_status=200
        )
        response_get_patched_movie = super_admin.api.movies_api.get_movie_by_id(
            movie_id=response_patch_movie.json()["id"], expected_status=200
        )
        ResponseMovie(**response_get_patched_movie.json())
        assert (
            response_get_patched_movie.json()["name"]
            == response_patch_movie.json()["name"]
        )
        assert (
            response_get_patched_movie.json()["price"]
            == response_patch_movie.json()["price"]
        )

    @allure.story("Корректность получения фильмов с параметрами в запросе")
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
        self, price, location, genreId, api_manager, movie_params
    ) -> None:

        movie_params["minPrice"] = price[0]
        movie_params["maxPrice"] = price[1]
        movie_params["locations"] = location
        movie_params["genreId"] = genreId
        response = api_manager.movies_api.get_movies(params=movie_params)
        response_data = response.json()
        ResponseGetMovie(**response_data)

        assert "movies" in response_data
        assert "count" in response_data

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
        self, super_admin: User, movie_data: dict[str, object], db_helper
    ):
        with allure.step("Попытка получить фильм из бд по имени"):
            assert db_helper.get_movie_by_name(movie_data["name"]) is None

        with allure.step("создание фильма по средствам API"):
            response = super_admin.api.movies_api.create_movie(movie_data)
            ResponseMovie(**response.json())

        with allure.step("Получение созданного фильма из бд по id"):
            assert db_helper.get_movie_by_id(response.json()["id"]) is not None

        with allure.step("Удаленеие фильма по средствам API"):
            response_deleted_movie = super_admin.api.movies_api.delete_movie_by_id(
                response.json()["id"]
            )
            ResponseMovie(**response_deleted_movie.json())

        with allure.step("Проверка что фильм удален из бд."):
            assert (
                db_helper.get_movie_by_id(response_deleted_movie.json()["id"]) is None
            )
