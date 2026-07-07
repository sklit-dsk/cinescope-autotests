import requests
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from clients.auth_api import AuthApi

session = requests.Session()
auth_api = AuthApi(session)

email = DataGenerator.generate_random_email()
fullName = f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}"
password = "12345678Aa"

class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        # добавим еше проверок
        assert "id" in response_data 
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        # assert response_data["user"]["email"] == registered_user["email"]

    def test_get_user_info(self, api_manager, authenticated_user):
        login_data = {
            "email": authenticated_user["email"],
            "password": authenticated_user["password"],
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()["user"]

        assert response_data["email"] == authenticated_user["email"]
        assert response_data["fullName"] == authenticated_user["fullName"]
