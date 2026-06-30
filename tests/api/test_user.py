import requests
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from clients.user_api import UserApi

session = requests.Session()
user_api = UserApi(session)

email = DataGenerator.generate_random_email()
fullName = f"{DataGenerator.generate_firstname()} {DataGenerator.generate_lastname()}"
password = "12345678Aa"

def test_get_user_info(user_id):
    response = user_api.get_user_info(user_id, expected_status=200)
    assert response.status_code == 200