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
            "password": registered_user["password"],
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        # assert response_data["user"]["email"] == registered_user["email"]

    def test_logout_user(self, api_manager, authenticated_user):
        login_data = {
            "email": authenticated_user["email"],
            "password": authenticated_user["password"],
        }
        api_manager.auth_api.login_user(login_data)

        response_logout = api_manager.auth_api.logout_user()
        assert response_logout.status_code == 200
