class TestUser:

    def test_get_user_info(self, authenticated_user, super_admin):
        response_user_info = super_admin.api.user_api.get_user_info(
            authenticated_user["id"], expected_status=200
        )

        assert authenticated_user["email"] == response_user_info.json()["email"]
        assert authenticated_user["id"] == response_user_info.json()["id"]

    def test_delete_user(self, authenticated_user, super_admin):
        response = super_admin.api.user_api.delete_user(
            user_id=authenticated_user["id"]
        )
        response_deleted_user_info = super_admin.api.user_api.get_user_info(
            user_id=authenticated_user["id"], expected_status=200
        )

        assert response.status_code == 200
        assert response_deleted_user_info.status_code == 200
        assert response_deleted_user_info.text == "{}"

    def test_patch_user(self, super_admin, authenticated_user):
        new_data = {
            "roles": ["USER", "ADMIN", "SUPER_ADMIN"],
            "verified": False,
            "banned": False,
        }
        response_before_patch = super_admin.api.user_api.get_user_info(
            user_id=authenticated_user["id"], expected_status=200
        )
        response = super_admin.api.user_api.patch_user_data(
            user_id=authenticated_user["id"], data=new_data, expected_status=200
        )

        assert response_before_patch.status_code == 200
        assert response.status_code == 200
        assert response_before_patch.json()["email"] == response.json()["email"]
        assert response_before_patch.json()["roles"] != response.json()["roles"]

    def test_create_user(self, user_data, super_admin):
        response = super_admin.api.user_api.create_user(
            data=user_data, expected_status=201
        )

        response_json = response.json()

        assert (
            response_json.get("id") and response_json["id"] != ""
        ), "ID должен быть не пустым"
        assert response_json.get("email") == user_data["email"]
        assert response_json.get("fullName") == user_data["fullName"]
        # assert response_json.get("roles", []) == user_data["roles"]
        assert response_json.get("verified") is True

    def test_get_list_users(self, user_params, super_admin):
        response = super_admin.api.user_api.get_list_users(
            expected_status=200, params=user_params
        )

        assert response.status_code == 200

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    def test_get_user_by_admin(self, admin, authenticated_user):

        response_user_info = admin.api.user_api.get_user_info(
            authenticated_user["id"], expected_status=200
        )

        assert authenticated_user["email"] == response_user_info.json()["email"]
        assert authenticated_user["id"] == response_user_info.json()["id"]
