from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

MOVIES = '/movies'

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies(self, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}",
            expected_status=expected_status,
            need_logging=False,
            **kwargs,
        )

    def create_movie(self, data, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=f"{MOVIES}",
            data=data,
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )

    def get_movie_by_id(self, movie_id, expected_status = None, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )

    def delete_movie_by_id(self, movie_id, expected_status = 200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )

    def patch_movie_by_id(self, movie_id, data, expected_status = 200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
            **kwargs,
        )
