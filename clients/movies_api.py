from typing import Any
from requests import Response, Session
from custom_requester.custom_requester import CustomRequester
from constants.base_urls import MOVIES_BASE_URL
from constants.endpoints import Endpoints

class MoviesApi(CustomRequester):

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies(self, expected_status: int = 200, **kwargs: Any) -> Response:
        return self.send_request(
            method="GET",
            endpoint=Endpoints.MOVIES.value,
            expected_status=expected_status,
            need_logging=False,
            **kwargs,
        )

    def create_movie(
        self, data: dict[str, object], expected_status: int = 201
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=Endpoints.MOVIES.value,
            data=data,
            expected_status=expected_status,
            need_logging=True,
        )

    def get_movie_by_id(
        self, movie_id: str, expected_status: int | None = None
    ) -> Response:
        return self.send_request(
            method="GET",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    def delete_movie_by_id(self, movie_id: str, expected_status: int = 200) -> Response:
        return self.send_request(
            method="DELETE",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    def patch_movie_by_id(
        self,
        movie_id: str,
        data: dict[str, object],
        expected_status: int = 200,
    ) -> Response:
        return self.send_request(
            method="PATCH",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
        )
