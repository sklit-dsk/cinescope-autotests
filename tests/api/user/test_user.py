class TestUser:
    def test_get_user_info(self, api_manager, authenticated_user, super_admin):
        response_user_info = api_manager.user_api.get_user_info(authenticated_user["id"], expected_status = 200)
            
        assert authenticated_user["email"] == response_user_info.json()["email"]
        assert authenticated_user["id"] == response_user_info.json()["id"]
            
    def test_delete_user(self, api_manager, authenticated_user, super_admin):
        response = api_manager.user_api.delete_user(user_id = authenticated_user["id"])
        response_deleted_user_info = api_manager.user_api.get_user_info(user_id = authenticated_user["id"], expected_status=200)
        
        assert response.status_code == 200
        assert response_deleted_user_info.status_code == 200
        assert response_deleted_user_info.text == "{}"
        
    def test_patch_user(self, api_manager, authenticated_user, super_admin):
        new_data = {
            "roles": [
                "USER",
                "ADMIN",
                "SUPER_ADMIN"
            ],
            "verified": False,
            "banned": False
        }
        response_before_patch = api_manager.user_api.get_user_info(user_id = authenticated_user["id"], expected_status=200)
        response = api_manager.user_api.patch_user_data(user_id = authenticated_user["id"], data = new_data, expected_status=200)
        
        assert response_before_patch.status_code == 200
        assert response.status_code == 200
        assert response_before_patch.json()["email"] == response.json()["email"]
        assert response_before_patch.json()["roles"] != response.json()["roles"]
        
    def test_create_user(self, api_manager, user_data, super_admin):
        response = api_manager.user_api.create_user(data = user_data, expected_status=201)
        
        assert response.status_code == 201
        assert response.json()["createdAt"]
        
    def test_get_list_users(self, api_manager, user_params, super_admin):
        response = api_manager.user_api.get_list_users(expected_status = 200, params = user_params)
        
        assert response.status_code == 200
        