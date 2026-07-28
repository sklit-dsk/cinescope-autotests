import pytest
from utils.data_generator import DataGenerator
from constants.roles import Roles

@pytest.fixture(scope="function")
def user_data() -> dict[str, object]:
    return DataGenerator.generate_user_data()


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
