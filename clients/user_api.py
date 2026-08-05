import allure
from typing import Any
from requests import Response, Session
from custom_requester.custom_requester import CustomRequester
from constants.base_urls import AUTH_BASE_URL
from models.base_models import TestUser
from constants.endpoints import Endpoints


class UserApi(CustomRequester):

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    @allure.step("Формирование запроса на получение данных пользователя")
    def get_user_info(
        self, user_id: str | None, expected_status: int | None = None
    ) -> Response:
        return self.send_request(
            method="GET",
            endpoint=f"{Endpoints.USER.value}/{user_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    @allure.step("Формирование запроса на удаление пользователя")
    def delete_user(self, user_id: str | None, expected_status: int = 200) -> Response:
        return self.send_request(
            method="DELETE",
            endpoint=f"{Endpoints.USER.value}/{user_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    @allure.step("Формирование запроса на изменение данных пользователя")
    def patch_user_data(
        self,
        user_id: str | None,
        data: dict[str, object],
        expected_status: int | None = None,
    ) -> Response:
        return self.send_request(
            method="PATCH",
            endpoint=f"{Endpoints.USER.value}/{user_id}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
        )

    @allure.step("Формирование запроса на создание пользователя")
    def create_user(
        self,
        data: TestUser,
        expected_status: int = 201,
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=f"{Endpoints.USER.value}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
        )

    @allure.step("Формирование запроса на получения списка пользователей")
    def get_list_users(self, expected_status: int | None = None, **kwargs) -> Response:
        return self.send_request(
            method="GET",
            endpoint=f"{Endpoints.USER.value}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )
