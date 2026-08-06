import allure
from typing import Any
from requests import Response, Session
from custom_requester.custom_requester import CustomRequester
from constants.base_urls import MOVIES_BASE_URL
from constants.endpoints import Endpoints
from models.movie_models import MovieModel, MovieParamsModel

class MoviesApi(CustomRequester):

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    @allure.step("Формирование GET запроса на получение фильмов")
    def get_movies(
        self, params: MovieParamsModel | None = None, expected_status: int = 200
    ) -> Response:
        return self.send_request(
            method="GET",
            endpoint=Endpoints.MOVIES.value,
            expected_status=expected_status,
            need_logging=False,
            params=params,
        )

    @allure.step("Формирование POST запроса на создание фильма")
    def create_movie(self, data: MovieModel, expected_status: int = 201) -> Response:
        return self.send_request(
            method="POST",
            endpoint=Endpoints.MOVIES.value,
            data=data,
            expected_status=expected_status,
            need_logging=True,
        )

    @allure.step("Формирование GET запроса на получение фильма по id")
    def get_movie_by_id(
        self, movie_id: int, expected_status: int | None = None
    ) -> Response:
        return self.send_request(
            method="GET",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    @allure.step("Формирование запроса DELETE на удаление фильма по id")
    def delete_movie_by_id(self, movie_id: int, expected_status: int = 200) -> Response:
        return self.send_request(
            method="DELETE",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    @allure.step("Формирование PAtch запрооса на изменения данных фильма по id")
    def patch_movie_by_id(
        self,
        movie_id: int,
        data: MovieModel,
        expected_status: int = 200,
    ) -> Response:
        return self.send_request(
            method="PATCH",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
        )
