import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


# @pytest.fixture(scope="function")
# def super_admin(api_manager):
#     login_data = {
#             "email": "api1@gmail.com",
#             "password": "asdqwe123Q",
#         }
#     api_manager.auth_api.login_user(login_data)
#     api_manager.auth_api.authenticate((login_data["email"], login_data["password"]))


@pytest.fixture(scope="function")
def authenticated_user(api_manager):
    # Create a test user
    password = DataGenerator.generate_random_password()
    test_user = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER", "ADMIN", "SUPER_ADMIN"],
    }

    # Register the user
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]

    # Authenticate the user
    api_manager.auth_api.authenticate((test_user["email"], test_user["password"]))

    yield test_user

    # Optionally, you can add cleanup code here to delete the user after the test if your API supports it.


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        Roles.SUPER_ADMIN.value,
        new_session,
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def common_user(user_session, super_admin, user_data):
    new_session = user_session()

    common_user = User(
        user_data["email"],
        user_data["password"],
        Roles.USER.value,
        new_session,
    )

    # ensure created user has USER role
    user_data["roles"] = [Roles.USER.value]
    super_admin.api.user_api.create_user(user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, user_data):
    new_session = user_session()

    admin = User(
        user_data["email"],
        user_data["password"],
        Roles.ADMIN.value,
        new_session,
    )

    # create user, then set ADMIN role via patch (some APIs ignore roles on create)
    user_data["roles"] = [Roles.ADMIN.value]
    created = super_admin.api.user_api.create_user(user_data)
    user_id = created.json().get("id")
    if user_id:
        super_admin.api.user_api.patch_user_data(
            user_id=user_id, data={"roles": [Roles.ADMIN.value]}, expected_status=200
        )
    admin.api.auth_api.authenticate(admin.creds)
    return admin
