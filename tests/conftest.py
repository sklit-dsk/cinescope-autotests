from typing import cast
from collections.abc import Callable, Generator
import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.base_models import TestUser

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
    api_manager: ApiManager, test_user: TestUser, super_admin: User
) -> Generator[TestUser, None, None]:

    response = api_manager.auth_api.register_user(test_user).json()
    test_user.id = response["id"]

    api_manager.auth_api.authenticate((test_user.email, test_user.password))

    yield test_user
    user_id = test_user.id
    assert user_id is not None
    super_admin.api.user_api.delete_user(user_id=user_id)


@pytest.fixture
def user_session() -> Generator[Callable[[], ApiManager], None, None]:
    user_pool: list[ApiManager] = []

    def _create_user_session() -> ApiManager:
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session: Callable[[], ApiManager]) -> User:
    new_session = user_session()

    username = SuperAdminCreds.USERNAME
    password = SuperAdminCreds.PASSWORD
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
            user_id=user_id, data={"roles": [Roles.ADMIN.value]}, expected_status=200
        )
    admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture
def test_user() -> TestUser:
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
def user_params() -> dict[str, object]:
    return DataGenerator.generate_user_params()


@pytest.fixture
def registration_user_data() -> dict[str, object]:
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value],
    }
