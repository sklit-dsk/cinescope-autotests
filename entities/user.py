from clients.api_manager import ApiManager
from models.base_models import LoginDataModel

class User:

    def __init__(
        self, email: str, password: str, roles: list[str], api: ApiManager
    ) -> None:
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self) -> LoginDataModel:
        return LoginDataModel(email=self.email, password=self.password)
