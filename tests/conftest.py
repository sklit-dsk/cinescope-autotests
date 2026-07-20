import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

    
@pytest.fixture(scope="function")
def super_admin(api_manager):
    login_data = {
            "email": "api1@gmail.com",
            "password": "asdqwe123Q",
        }
    api_manager.auth_api.login_user(login_data)
    api_manager.auth_api.authenticate((login_data["email"], login_data["password"]))
    
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
    
