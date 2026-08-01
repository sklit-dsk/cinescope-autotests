import allure
import pytest
from clients.api_manager import ApiManager
from models.base_models import RegisterUserResponse, AuthResponse
from models.base_models import TestUser
from venv import logger

@allure.epic("Тестирование авторизации")
@allure.feature("Тестирование операций с пользователями")
@allure.label("qa_name", "Danila")
class TestAuth:

    @allure.story("Корректность регистрации пользователя")
    @allure.description("""
        Этот тест проверяет корректность регистрации пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест регистрации пользователя")
    @pytest.mark.api
    def test_register_user(self, api_manager: ApiManager, test_user: TestUser) -> None:
        response = api_manager.auth_api.register_user(user_data=test_user)
        logger.info(f"{response.json()}")
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    @allure.story("Корректность регистрации и входа пользователя")
    @allure.description("""
        Этот тест проверяет корректность регистрации и входа пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест регистрации и входа пользователя")
    @pytest.mark.api
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

    @allure.story("Корректность выхода пользователя")
    @allure.description("""
        Этот тест проверяет корректность выхода пользователя из системы.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест выхода пользователя")
    @pytest.mark.api
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
