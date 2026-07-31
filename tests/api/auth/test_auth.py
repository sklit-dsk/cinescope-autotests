from clients.api_manager import ApiManager
from models.base_models import RegisterUserResponse, AuthResponse
from models.base_models import TestUser
from venv import logger
from constants.roles import Roles
from datetime import datetime


class TestAuth:

    def test_register_user(self, api_manager: ApiManager, test_user: TestUser) -> None:
        response = api_manager.auth_api.register_user(user_data=test_user)
        logger.info(f"{response.json()}")
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_register_and_login_user(
        self, api_manager: ApiManager, registered_user: TestUser
    ) -> None:
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password,
        }
        response = api_manager.auth_api.login_user(login_data)
        logger.info(f"{response.json()}")
        login_user_response = AuthResponse(**response.json())
        assert registered_user.email == login_user_response.user.email

    def test_logout_user(
        self, api_manager: ApiManager, authenticated_user: TestUser
    ) -> None:
        login_data = {
            "email": authenticated_user.email,
            "password": authenticated_user.password,
        }
        response_login = api_manager.auth_api.login_user(login_data)
        AuthResponse(**response_login.json())
        response_logout = api_manager.auth_api.logout_user()
        logger.info(f"{response_logout.text}")
        assert response_logout.status_code == 200
