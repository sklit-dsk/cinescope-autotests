from collections.abc import Generator
import requests
import pytest
from entities.user import User
from utils.data_generator import DataGenerator


@pytest.fixture(scope="function")
def movie_params() -> dict[str, object]:
    return DataGenerator.generate_movie_params()


@pytest.fixture(scope="function")
def bad_movie_params() -> dict[str, object]:
    return DataGenerator.generate_bad_movie_params()


@pytest.fixture(scope="function")
def movie_data() -> dict[str, object]:
    return DataGenerator.generate_movie_data()


@pytest.fixture(scope="function")
def created_movie(
    super_admin: User, movie_data: dict[str, object]
) -> Generator[requests.Response, None, None]:
    response = super_admin.api.movies_api.create_movie(movie_data)
    response_movie = super_admin.api.movies_api.get_movie_by_id(response.json()["id"])
    yield response_movie
    response_delete_movie = super_admin.api.session.request(
        "DELETE",
        f"{super_admin.api.movies_api.base_url}/movies/{response.json()['id']}",
    )
    if response_delete_movie.status_code not in (200, 404):
        raise ValueError(
            f"Unexpected status code during cleanup: {response_delete_movie.status_code}"
        )
