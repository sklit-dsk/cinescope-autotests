import allure
from typing import Any
from requests import Response, Session
from custom_requester.custom_requester import CustomRequester
from constants.base_urls import AUTH_BASE_URL
from constants.endpoints import Endpoints

class AuthApi(CustomRequester):

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def register_user(self, user_data: Any, expected_status: int = 201) -> Response:
        with allure.step("Формирование запроса на регимтрацию пользователя"):
            return self.send_request(
                method="POST",
                endpoint=Endpoints.REGISTER.value,
                data=user_data,
                expected_status=expected_status,
            )

    def login_user(
        self, login_data: dict[str, str], expected_status: int = 201
    ) -> Response:
        with allure.step("Формирование запроса на логин пользователя"):
            return self.send_request(
                method="POST",
                endpoint=Endpoints.LOGIN.value,
                data=login_data,
                expected_status=expected_status,
            )

    def authenticate(self, user_creds: tuple[str, str]) -> None:
        with allure.step("Аутентификация пользователя"):
            with allure.step("Установка данных пользователя"):
                login_data = {"email": user_creds[0], "password": user_creds[1]}
            with allure.step("Логин пользователя"):
                response = self.login_user(login_data).json()
                if "accessToken" not in response:
                    raise KeyError("token is missing")
                token = response["accessToken"]
            with allure.step("Обновление заголовков с токеном авторизации"):
                self._update_session_headers({"authorization": "Bearer " + token})

    def logout_user(self, expected_status: int = 200) -> Response:
        with allure.step("Формирование запроса на логаут пользователя"):
            return self.send_request(
                method="GET",
                endpoint=Endpoints.LOGOUT.value,
                expected_status=expected_status,
            )
