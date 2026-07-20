import pytest
from utils.data_generator import DataGenerator

@pytest.fixture(scope="function")
def user_data():
    return DataGenerator.generate_user_data()

@pytest.fixture(scope="function")
def user_params():
    return DataGenerator.generate_user_params()