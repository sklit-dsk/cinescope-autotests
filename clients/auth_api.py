import allure
from typing import Any
from requests import Response, Session
from custom_requester.custom_requester import CustomRequester
from constants.base_urls import AUTH_BASE_URL
from constants.endpoints import Endpoints
from models.base_models import LoginDataModel, TestUser

class AuthApi(CustomRequester):

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    @allure.step("Формирование запроса на регимтрацию пользователя")
    def register_user(
        self, user_data: TestUser, expected_status: int = 201
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=Endpoints.REGISTER.value,
            data=user_data,
            expected_status=expected_status,
        )

    @allure.step("Формирование запроса на логин пользователя")
    def login_user(
        self, login_data: LoginDataModel, expected_status: int = 201
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=Endpoints.LOGIN.value,
            data=login_data,
            expected_status=expected_status,
        )

    @allure.step("Аутентификация пользователя")
    def authenticate(self, user_creds: LoginDataModel) -> None:
        with allure.step("Установка данных пользователя"):
            login_data = LoginDataModel(
                email=user_creds.email, password=user_creds.password
            )
        with allure.step("Логин пользователя"):
            response = self.login_user(login_data).json()
            assert "accessToken" in response, "token is missing"
            token = response["accessToken"]
        with allure.step("Обновление заголовков с токеном авторизации"):
            self._update_session_headers({"authorization": "Bearer " + token})

    @allure.step("Формирование запроса на логаут пользователя")
    def logout_user(self, expected_status: int = 200) -> Response:
        return self.send_request(
            method="GET",
            endpoint=Endpoints.LOGOUT.value,
            expected_status=expected_status,
        )
