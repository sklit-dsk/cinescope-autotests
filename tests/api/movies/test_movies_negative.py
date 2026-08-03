import allure
import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from models.movie_models import MovieParamsModel, MovieModel, ResponseMovie
from entities.user import User
from typing import Any

@allure.epic("Тестирование фильмов")
@allure.feature("Негативные сценарии фильмов")
@allure.label("qa_name", "Danila")
class TestMoviesNegative:

    @allure.story("Корректность получения фильмов при плохих параметрах")
    @allure.description("""
        Этот тест проверяет корректность обработки некорректных параметров запроса.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильмов с некорректными параметрами")
    @pytest.mark.api
    def test_get_movies_with_bad_params(
        self, api_manager: ApiManager, bad_movie_params: MovieParamsModel
    ) -> None:
        with allure.step("Попытка получить фильмы с невалидными параметрами запроса"):
            response = api_manager.movies_api.get_movies(
                expected_status=400, params=bad_movie_params
            )
            assert response.json()["error"]

    @allure.story("Корректность создания фильма с плохими данными")
    @allure.description("""
        Этот тест проверяет, что создание фильма с некорректными данными отклоняется.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания фильма с некорректными данными")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "name,price,description",
        [
            (144122, "dasdsad", 133),
            (132233, 15, "dasdsadas"),
            ("asfaa", "dasdad", "dadassa"),
            ("aqdas", 2342, 334),
        ],
    )
    def test_create_movie_with_bad_params(
        self,
        movie_data: MovieModel,
        super_admin: User,
        name: Any,
        price: Any,
        description: Any,
    ) -> None:
        with allure.step("Присвоение новых данных фильма"):
            movie_data.name = name
            movie_data.price = price
            movie_data.description = description

        with allure.step("Попытка создания фильма с невалидными данными"):
            super_admin.api.movies_api.create_movie(movie_data, expected_status=400)

    @allure.story("Тест создания уже существующего фильма")
    @allure.description("""
        Этот тест проверяет, что нельзя создать уже существующий фильм.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания уже существующего фильма")
    @pytest.mark.api
    @pytest.mark.flaky(reruns=3)
    def test_create_existing_movie(
        self,
        created_movie: ResponseMovie,
        super_admin: User,
        movie_data: MovieModel,
    ) -> None:
        with allure.step("Попытка создания существующего фильма"):
            super_admin.api.movies_api.create_movie(movie_data, expected_status=409)

        assert created_movie.name == movie_data.name

    @allure.story("Тест получения несуществующего фильма")
    @allure.description("""
        Этот тест проверяет получение несуществующего фильма после удаления.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения несуществующего фильма")
    @pytest.mark.api
    def test_get_non_existent_movie(
        self, super_admin: User, created_movie: ResponseMovie
    ) -> None:
        with allure.step("Удаление фильма по id"):
            response_delete_movie = super_admin.api.movies_api.delete_movie_by_id(
                movie_id=created_movie.id
            )
        with allure.step("Попытка получить удаленный фильм"):
            super_admin.api.movies_api.get_movie_by_id(
                movie_id=response_delete_movie.json()["id"], expected_status=404
            )

    @allure.story("Корректность удаления несуществующего фильма")
    @allure.description("""
        Этот тест проверяет, что повторное удаление фильма возвращает ошибку.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления несуществующего фильма")
    @pytest.mark.api
    def test_delete_non_existent_movie(
        self, super_admin: User, created_movie: ResponseMovie
    ) -> None:
        with allure.step("Удаление фильма"):
            super_admin.api.movies_api.delete_movie_by_id(movie_id=created_movie.id)
        with allure.step("Попытка удалить несуществующий фильм"):
            super_admin.api.movies_api.delete_movie_by_id(
                movie_id=created_movie.id, expected_status=404
            )

    @allure.story("Корректность удаления фильма администратором")
    @allure.description("""
        Этот тест проверяет, что администратор не может удалить фильм.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма администратором")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "name,price,location,genreId",
        [
            (
                DataGenerator.generate_movie_name(),
                DataGenerator.generate_min_price(),
                DataGenerator.generate_location(),
                DataGenerator.generate_genre_id(),
            ),
            (
                DataGenerator.generate_movie_name(),
                DataGenerator.generate_min_price(),
                DataGenerator.generate_location(),
                DataGenerator.generate_genre_id(),
            ),
            (
                DataGenerator.generate_movie_name(),
                DataGenerator.generate_min_price(),
                DataGenerator.generate_location(),
                DataGenerator.generate_genre_id(),
            ),
        ],
        ids=["case_SPB_1", "case_MSK", "case_SPB_2"],
    )
    @pytest.mark.flaky(reruns=3)
    def test_delete_movie_admin(
        self,
        admin: User,
        super_admin: User,
        name: str,
        price: int,
        location: str,
        genreId: int,
    ) -> None:
        with allure.step("Генерация параметризированных данных для фильма"):
            movie_data = MovieModel(
                name=name,
                imageUrl=DataGenerator.generate_movie_image_url(),
                price=price,
                description=DataGenerator.generate_movie_description(),
                location=location,
                published=DataGenerator.generate_published(),
                genreId=genreId,
            )
        with allure.step("Создание фильма супер админом"):
            response = ResponseMovie(
                **super_admin.api.movies_api.create_movie(movie_data).json()
            )
        with allure.step("Попытка удаления фильма пользователем с ролью Админ"):
            admin.api.movies_api.delete_movie_by_id(
                movie_id=response.id, expected_status=403
            )

    @allure.story("Корректность удаления фильма обычным пользователем")
    @allure.description("""
        Этот тест проверяет, что обычный пользователь не может удалить фильм.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма обычным пользователем")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "name,price,location,genreId",
        [
            (DataGenerator.generate_movie_name(), 1000, "SPB", 7),
            (DataGenerator.generate_movie_name(), 900, "MSK", 8),
            (DataGenerator.generate_movie_name(), 800, "SPB", 9),
        ],
        ids=["case_SPB_1", "case_MSK", "case_SPB_2"],
    )
    def test_delete_movie_common_user(
        self,
        common_user: User,
        super_admin: User,
        name: str,
        price: int,
        location: str,
        genreId: int,
    ) -> None:
        with allure.step("Генерация параметризированных данных для фильма"):
            movie_data = MovieModel(
                name=name,
                imageUrl=DataGenerator.generate_movie_image_url(),
                price=price,
                description=DataGenerator.generate_movie_description(),
                location=location,
                published=DataGenerator.generate_published(),
                genreId=genreId,
            )
        with allure.step("Создание фильма супер админом"):
            response = ResponseMovie(
                **super_admin.api.movies_api.create_movie(movie_data).json()
            )
        with allure.step("Попытка удаления фильма пользователем с ролью User"):
            common_user.api.movies_api.delete_movie_by_id(
                movie_id=response.id, expected_status=403
            )
