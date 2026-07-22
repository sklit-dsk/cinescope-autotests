import pytest
from utils.data_generator import DataGenerator

@pytest.fixture(scope="function")
def movie_params():
    return DataGenerator.generate_movie_params()

@pytest.fixture(scope="function")
def bad_movie_params():
    return DataGenerator.generate_bad_movie_params()

@pytest.fixture(scope="function")
def movie_data():
    return DataGenerator.generate_movie_data()


@pytest.fixture(scope="function")
def created_movie(super_admin, movie_data):
    response = super_admin.api.movies_api.create_movie(movie_data)
    yield response
    response_delete_movie = super_admin.api.session.request(
        "DELETE",
        f"{super_admin.api.movies_api.base_url}/movies/{response.json()['id']}",
    )
    if response_delete_movie.status_code not in (200, 404):
        raise ValueError(
            f"Unexpected status code during cleanup: {response_delete_movie.status_code}"
        )
