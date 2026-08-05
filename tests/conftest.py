import time
import requests
import pytest
import allure
from pytest_check import check
from typing import cast
from collections.abc import Callable, Generator
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.base_models import (
    TestUser,
    RegisterUserResponse,
    UserParamsModel,
    LoginDataModel,
)
from sqlalchemy.orm.session import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from uuid import uuid4
from db_models.user import UserDBModel
from datetime import datetime

@pytest.fixture(scope="session")
def session() -> Generator[requests.Session, None, None]:
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session: requests.Session) -> ApiManager:
    return ApiManager(session)


@pytest.fixture(scope="function")
def authenticated_user(
    api_manager: ApiManager,
    test_user: TestUser,
    super_admin: User,
    request: pytest.FixtureRequest,
) -> Generator[TestUser, None, None]:
    with allure.step("Регистрация пользователя"):
        response = RegisterUserResponse(
            **api_manager.auth_api.register_user(test_user).json()
        )
    test_user.id = response.id
    with allure.step("Аутентификация тестового пользователя"):
        api_manager.auth_api.authenticate(
            LoginDataModel(email=test_user.email, password=test_user.password)
        )

    yield test_user
    if request.node.get_closest_marker("skip_authenticated_user_cleanup") is not None:
        return
    with allure.step("Очистка пользователя после теста"):
        user_id = test_user.id
        assert user_id is not None
        super_admin.api.user_api.delete_user(user_id=user_id)


@pytest.fixture
def user_session() -> Generator[Callable[[], ApiManager], None, None]:
    with allure.step("Создание пользовательской сессии"):
        user_pool: list[ApiManager] = []

        def _create_user_session() -> ApiManager:
            session = requests.Session()
            user_session = ApiManager(session)
            user_pool.append(user_session)
            return user_session

    yield _create_user_session
    with allure.step("Закрытие всех сессий пользователей после теста"):
        for user in user_pool:
            user.close_session()


@pytest.fixture
def super_admin(user_session: Callable[[], ApiManager]) -> User:
    new_session = user_session()
    with allure.step("Создание пользователя с ролью SUPER ADMIN"):
        username = SuperAdminCreds.USERNAME
        password = SuperAdminCreds.PASSWORD
        with check:
            assert username is not None
            assert password is not None

        super_admin = User(
            cast(str, username),
            cast(str, password),
            [Roles.SUPER_ADMIN.value],
            new_session,
        )

        super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def common_user(
    user_session: Callable[[], ApiManager],
    super_admin: User,
    user_data: TestUser,
) -> User:
    new_session = user_session()
    with allure.step("Создание пользователя с ролью USER"):
        email = user_data.email
        password = user_data.password

        common_user = User(
            cast(str, email),
            cast(str, password),
            [Roles.USER.value],
            new_session,
        )

        user_data.roles = [Roles.USER.value]
        super_admin.api.user_api.create_user(user_data)
        common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(
    user_session: Callable[[], ApiManager],
    super_admin: User,
    user_data: TestUser,
) -> User:
    new_session = user_session()
    with allure.step("Создание пользователя с ролью ADMIN"):
        email = user_data.email
        password = user_data.password

        admin = User(
            cast(str, email),
            cast(str, password),
            [Roles.ADMIN.value],
            new_session,
        )

        user_data.roles = [Roles.ADMIN.value]
        created = super_admin.api.user_api.create_user(user_data)
        user_id = created.json().get("id")
        if user_id:
            super_admin.api.user_api.patch_user_data(
                user_id=user_id,
                data={"roles": [Roles.ADMIN.value]},
                expected_status=200,
            )
        admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture
def test_user() -> TestUser:
    with allure.step("Генерация и валидация данных тестового юзера"):
        random_password = DataGenerator.generate_random_password()
        return TestUser(
            email=DataGenerator.generate_random_email(),
            fullName=DataGenerator.generate_random_name(),
            password=random_password,
            passwordRepeat=random_password,
            roles=[Roles.USER.value],
        )


@pytest.fixture(scope="function")
def registered_user(api_manager: ApiManager, test_user: TestUser) -> TestUser:
    with allure.step("Регистрация и возврат тестового юзера"):
        response = api_manager.auth_api.register_user(test_user).json()
        test_user.id = response["id"]
        return test_user


@pytest.fixture(scope="session")
def unauthenticated_api_manager() -> Generator[ApiManager, None, None]:
    http_session = requests.Session()
    yield ApiManager(http_session)
    http_session.close()


@pytest.fixture(scope="function")
def user_data() -> TestUser:
    with allure.step("Генерация и валидация данных пользователя"):
        password = DataGenerator.generate_random_password()
        return TestUser(
            email=DataGenerator.generate_random_email(),
            fullName=DataGenerator.generate_random_name(),
            password=password,
            passwordRepeat=password,
            verified=DataGenerator.generate_verification(),
            banned=False,
        )


@pytest.fixture(scope="function")
def user_params() -> UserParamsModel:
    with allure.step(
        "Генерация и валидация параметров запроса на получение пользователей"
    ):
        return UserParamsModel(
            pageSize=DataGenerator.generate_page_size(),
            page=DataGenerator.generate_page_size(),
            roles=DataGenerator.generate_roles(),
            createdAt=DataGenerator.generate_created_at(),
        )


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    with allure.step("Создание и возврат сессии для работы с базой данных"):
        db_session = get_db_session()
        yield db_session
        db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session: Session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper: DBHelper) -> Generator[UserDBModel, None, None]:
    test_user_data = UserDBModel(
        id=f"{uuid4()}",  # генерируем UUID как строку
        email=DataGenerator.generate_random_email(),
        full_name=DataGenerator.generate_random_name(),
        password=DataGenerator.generate_random_password(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        verified=False,
        banned=False,
        roles="{USER}",
    )
    with allure.step("Создание тестового пользователя в БД"):
        user = db_helper.create_test_user(test_user_data)
        yield user
    with allure.step("Удаление тестового пользователя из БД после теста"):
        user_id = cast(str, user.id)
        if db_helper.get_user_by_id(user_id):
            db_helper.delete_user(user)


@pytest.fixture
def delay_between_retries() -> Generator[None, None, None]:
    time.sleep(2)
    yield
