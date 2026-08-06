import allure
import pytest
from clients.api_manager import ApiManager
from models.base_models import (
    RegisterUserResponse,
    AuthResponse,
    LoginDataModel,
    TestUser,
)
from pytest_check import check

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
        with allure.step("Регистрация пользователя"):
            response = RegisterUserResponse(
                **api_manager.auth_api.register_user(user_data=test_user).json()
            )
        with check:
            assert response.email == test_user.email, "Email не совпадает"

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
        with allure.step("Подготовка данных для логина пользователя"):
            login_data = LoginDataModel(
                email=registered_user.email,
                password=registered_user.password,
            )
        with allure.step("Логин пользователя"):
            response = AuthResponse(
                **api_manager.auth_api.login_user(login_data).json()
            )
        with check:
            assert registered_user.email == response.user.email

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
        with allure.step("Подготовка данных для логина пользователя"):
            login_data = LoginDataModel(
                email=authenticated_user.email,
                password=authenticated_user.password,
            )
        with allure.step("Логин пользователя"):
            AuthResponse(**api_manager.auth_api.login_user(login_data).json())
        with allure.step("Логаут пользователя"):
            response_logout = api_manager.auth_api.logout_user()
        with check:
            assert response_logout.status_code == 200
