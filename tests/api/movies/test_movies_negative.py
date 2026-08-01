import allure
import pytest
from utils.data_generator import DataGenerator


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
    def test_get_movies_with_bad_params(self, api_manager, bad_movie_params) -> None:
        response = api_manager.movies_api.get_movies(
            expected_status=400, params=bad_movie_params
        )
        response_data = response.json()
        assert response_data["error"]

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
        movie_data,
        super_admin,
        name: str,
        price: int,
        description: str,
    ) -> None:
        movie_data["name"] = name
        movie_data["price"] = price
        movie_data["description"] = description

        super_admin.api.movies_api.create_movie(movie_data, expected_status=400)

    @allure.story("Корректность создания уже существующего фильма")
    @allure.description("""
        Этот тест проверяет, что нельзя создать уже существующий фильм.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания уже существующего фильма")
    @pytest.mark.api
    @pytest.mark.flaky(reruns=3)
    def test_create_existing_movie(
        self, created_movie, super_admin, movie_data
    ) -> None:

        response = created_movie.json()
        super_admin.api.movies_api.create_movie(movie_data, expected_status=409)

        assert response["name"] == movie_data["name"]

    @allure.story("Корректность получения несуществующего фильма")
    @allure.description("""
        Этот тест проверяет получение несуществующего фильма после удаления.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения несуществующего фильма")
    @pytest.mark.api
    def test_get_non_existent_movie(self, super_admin, created_movie) -> None:
        response = created_movie.json()
        response_delete_movie = super_admin.api.movies_api.delete_movie_by_id(
            movie_id=response["id"]
        )
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
    def test_delete_non_existent_movie(self, super_admin, created_movie) -> None:
        response = created_movie.json()
        super_admin.api.movies_api.delete_movie_by_id(movie_id=response["id"])
        super_admin.api.movies_api.delete_movie_by_id(
            movie_id=response["id"], expected_status=404
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
        self, admin, super_admin, name, price, location, genreId
    ) -> None:
        movie_data = {
            "name": name,
            "imageUrl": DataGenerator.generate_movie_image_url(),
            "price": price,
            "description": DataGenerator.generate_movie_description(),
            "location": location,
            "published": DataGenerator.generate_published(),
            "genreId": genreId,
        }
        response = super_admin.api.movies_api.create_movie(movie_data)
        admin.api.movies_api.delete_movie_by_id(
            movie_id=response.json()["id"], expected_status=403
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
        self, common_user, super_admin, name, price, location, genreId
    ) -> None:
        movie_data = {
            "name": name,
            "imageUrl": DataGenerator.generate_movie_image_url(),
            "price": price,
            "description": DataGenerator.generate_movie_description(),
            "location": location,
            "published": DataGenerator.generate_published(),
            "genreId": genreId,
        }
        response = super_admin.api.movies_api.create_movie(movie_data)
        common_user.api.movies_api.delete_movie_by_id(
            movie_id=response.json()["id"], expected_status=403
        )
