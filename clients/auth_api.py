from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL

LOGIN = '/login'
REGISTER = '/register'
LOGOUT = '/logout'


class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)
        
    def register_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=REGISTER,
            data=user_data,
            expected_status=expected_status
        )
    
    def login_user(self, login_data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint=LOGIN,
            data=login_data,
            expected_status=expected_status
        )