import pytest
import allure
from models.base_models import RegisterUserResponse, TestUser as TestUserModel
from venv import logger


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
        self, authenticated_user: TestUserModel, super_admin
    ) -> None:
        logger.info(f"{authenticated_user}")
        response = super_admin.api.user_api.get_user_info(
            authenticated_user.id, expected_status=200
        )
        logger.info(f"{response.json()}")
        response_user_info = RegisterUserResponse(**response.json())

        assert response_user_info.email == authenticated_user.email

    @allure.story("Корректность удаления пользователя")
    @allure.description("""
        Этот тест проверяет корректность удаления пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления пользователя")
    @pytest.mark.api
    def test_delete_user(self, authenticated_user: TestUserModel, super_admin) -> None:
        response = super_admin.api.user_api.delete_user(user_id=authenticated_user.id)
        assert response.status_code == 200
        response_deleted_user_info = super_admin.api.user_api.get_user_info(
            user_id=authenticated_user.email, expected_status=200
        )
        assert response.status_code == 200
        assert response_deleted_user_info.text == "{}"

    @allure.story("Корректность обновления пользователя")
    @allure.description("""
        Этот тест проверяет корректность обновления пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест обновления пользователя")
    @pytest.mark.api
    def test_patch_user(self, super_admin, authenticated_user: TestUserModel) -> None:
        new_data = {
            "roles": ["USER", "ADMIN", "SUPER_ADMIN"],
            "verified": False,
            "banned": False,
        }
        response_before_patch = super_admin.api.user_api.get_user_info(
            user_id=authenticated_user.id, expected_status=200
        )
        response = super_admin.api.user_api.patch_user_data(
            user_id=authenticated_user.id, data=new_data, expected_status=200
        )

        assert response_before_patch.status_code == 200
        assert response.status_code == 200
        assert response_before_patch.json()["email"] == response.json()["email"]
        assert response_before_patch.json()["roles"] != response.json()["roles"]

    @allure.story("Корректность создания пользователя")
    @allure.description("""
        Этот тест проверяет корректность создания пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания пользователя")
    @pytest.mark.api
    def test_create_user(self, user_data, super_admin) -> None:
        response = super_admin.api.user_api.create_user(
            data=user_data, expected_status=201
        )

        RegisterUserResponse(**response.json())

    @allure.story("Корректность получения списка пользователей")
    @allure.description("""
        Этот тест проверяет корректность получения списка пользователей.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения списка пользователей")
    @pytest.mark.api
    def test_get_list_users(self, user_params, super_admin) -> None:
        response = super_admin.api.user_api.get_list_users(
            expected_status=200, params=user_params
        )
        logger.info(response.json())

    @allure.story("Корректность получения пользователя обычным пользователем")
    @allure.description("""
        Этот тест проверяет корректность запрета доступа обычного пользователя к данным другого пользователя.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения пользователя обычным пользователем")
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user) -> None:
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    @allure.story("Корректность получения пользователя администратором")
    @allure.description("""
        Этот тест проверяет корректность получения пользователя администратором.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения пользователя администратором")
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_user_by_admin(self, admin, authenticated_user: TestUserModel) -> None:

        response_user_info = admin.api.user_api.get_user_info(
            authenticated_user.id, expected_status=200
        )
        RegisterUserResponse(**response_user_info.json())
        assert authenticated_user.email == response_user_info.json()["email"]
        assert authenticated_user.id == response_user_info.json()["id"]
