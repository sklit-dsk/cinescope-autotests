from venv import logger

import pytest
from utils.data_generator import DataGenerator
from entities.user import User

class TestMovies:

    def test_get_movies_without_params(self, api_manager) -> None:
        response = api_manager.movies_api.get_movies()
        response_data = response.json()

        assert "count" in response_data
        assert response_data["movies"]

    def test_get_movies_with_params(self, api_manager, movie_params) -> None:
        response = api_manager.movies_api.get_movies(params=movie_params)
        response_data = response.json()

        assert "movies" in response_data
        assert "count" in response_data

    def test_create_movie(self, created_movie) -> None:
        response = created_movie.json()
        assert response["createdAt"]

    def test_get_movie_by_id(self, super_admin, created_movie) -> None:
        response = created_movie
        response_movie = super_admin.api.movies_api.get_movie_by_id(
            movie_id=response.json()["id"], expected_status=200
        )

        assert response.json()["id"] == response_movie.json()["id"]

    def test_delete_movie(self, super_admin, created_movie) -> None:
        response = created_movie.json()
        response_delete_movie = super_admin.api.movies_api.delete_movie_by_id(
            movie_id=response["id"]
        )
        super_admin.api.movies_api.get_movie_by_id(
            movie_id=response_delete_movie.json()["id"], expected_status=404
        )

    def test_patch_movie(self, super_admin, created_movie, movie_data) -> None:
        response = created_movie.json()
        new_movie_data = movie_data.copy()
        new_movie_data["name"] = DataGenerator.generate_movie_name()
        new_movie_data["price"] = DataGenerator.generate_min_price()
        response_patch_movie = super_admin.api.movies_api.patch_movie_by_id(
            movie_id=response["id"], data=new_movie_data, expected_status=200
        )
        response_get_patched_movie = super_admin.api.movies_api.get_movie_by_id(
            movie_id=response_patch_movie.json()["id"], expected_status=200
        )

        assert (
            response_get_patched_movie.json()["name"]
            == response_patch_movie.json()["name"]
        )
        assert (
            response_get_patched_movie.json()["price"]
            == response_patch_movie.json()["price"]
        )

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

        assert "movies" in response_data
        assert "count" in response_data

    @pytest.mark.flaky(reruns=3)
    def test_create_and_delete_movie_and_check_db(
        self, super_admin: User, movie_data: dict[str, object], db_helper
    ):
        assert db_helper.get_movie_by_name(movie_data["name"]) is None
        response = super_admin.api.movies_api.create_movie(movie_data)
        logger.info(response.json())
        assert db_helper.get_movie_by_id(response.json()["id"]) is not None
        response_deleted_movie = super_admin.api.movies_api.delete_movie_by_id(
            response.json()["id"]
        )
        logger.info(response_deleted_movie.json())
        assert db_helper.get_movie_by_id(response_deleted_movie.json()["id"]) is None
