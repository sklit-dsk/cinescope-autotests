import pytest
import allure
from models.base_models import RegisterUserResponse, TestUser, UserParamsModel
from venv import logger
from entities.user import User
from pytest_check import check

@allure.epic("Тестирование пользователей")
@allure.feature("Тестирование операций с пользователями")
@allure.label("qa_name", "Danila")
class TestUserApiTests:

    @allure.story("Корректность получения пользователя по id")
    @allure.description("""
        Этот тест проверяет корректность получения пользователя по id.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения пользователя по id")
    @pytest.mark.api
    def test_get_user_info(
        self, authenticated_user: TestUser, super_admin: User
    ) -> None:
        with allure.step("Получение пользователя по id"):
            response = RegisterUserResponse(
                **super_admin.api.user_api.get_user_info(
                    authenticated_user.id, expected_status=200
                ).json()
            )
        with check:
            check.equal(response.email, authenticated_user.email)

    @allure.story("Корректность удаления пользователя")
    @allure.description("""
        Этот тест проверяет корректность удаления пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления пользователя")
    @pytest.mark.api
    @pytest.mark.skip_authenticated_user_cleanup
    def test_delete_user(self, authenticated_user: TestUser, super_admin: User) -> None:
        with allure.step("Запрос на удаление пользователя"):
            super_admin.api.user_api.delete_user(
                user_id=authenticated_user.id, expected_status=200
            )

    @allure.story("Корректность обновления пользователя")
    @allure.description("""
        Этот тест проверяет корректность обновления пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест обновления пользователя")
    @pytest.mark.api
    def test_patch_user(self, super_admin: User, authenticated_user: TestUser) -> None:
        with allure.step("Создание новых данных для изменения"):
            new_data = {
                "roles": ["USER", "ADMIN", "SUPER_ADMIN"],
                "verified": False,
                "banned": False,
            }
        with allure.step("Получение пользователя до изменения данных"):
            response_before_patch = RegisterUserResponse(
                **super_admin.api.user_api.get_user_info(
                    user_id=authenticated_user.id, expected_status=200
                ).json()
            )
        with allure.step("Изменение данных пользователя"):
            response = RegisterUserResponse(
                **super_admin.api.user_api.patch_user_data(
                    user_id=authenticated_user.id, data=new_data, expected_status=200
                ).json()
            )
        logger.info(response.model_dump())
        with check:
            assert response_before_patch.email == response.email
            assert response_before_patch.roles != response.roles

    @allure.story("Корректность создания пользователя")
    @allure.description("""
        Этот тест проверяет корректность создания пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания пользователя")
    @pytest.mark.api
    def test_create_user(self, user_data: TestUser, super_admin: User) -> None:
        with allure.step("Создание пользователя"):
            RegisterUserResponse(
                **super_admin.api.user_api.create_user(
                    data=user_data, expected_status=201
                ).json()
            )

    @allure.story("Корректность получения списка пользователей")
    @allure.description("""
        Этот тест проверяет корректность получения списка пользователей.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения списка пользователей")
    @pytest.mark.api
    def test_get_list_users(
        self, user_params: UserParamsModel, super_admin: User
    ) -> None:
        with allure.step("Получение пользователей по передаваемым параметрам"):
            super_admin.api.user_api.get_list_users(
                expected_status=200, params=user_params
            )

    @allure.story("Корректность получения пользователя обычным пользователем")
    @allure.description("""
        Этот тест проверяет корректность запрета доступа обычного пользователя к данным другого пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения пользователя обычным пользователем")
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user: User) -> None:
        with allure.step("Попытка получения пользователя обычным юзером"):
            common_user.api.user_api.get_user_info(
                common_user.email, expected_status=403
            )

    @allure.story("Корректность получения пользователя администратором")
    @allure.description("""
        Этот тест проверяет корректность получения пользователя администратором.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения пользователя администратором")
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_user_by_admin(self, admin: User, authenticated_user: TestUser) -> None:
        with allure.step("Получение полтьзователя с ролью Admin"):
            response_user_info = RegisterUserResponse(
                **admin.api.user_api.get_user_info(
                    authenticated_user.id, expected_status=200
                ).json()
            )
        with check:
            assert authenticated_user.email == response_user_info.email
            assert authenticated_user.id == response_user_info.id
