from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL

USER = '/user'


class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def get_user_info(self, user_id, expected_status=None, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )

    def delete_user(self, user_id, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )

    def delete_users(self, *user_ids, **kwargs):
        for user_id in user_ids:
            self.delete_user(user_id, **kwargs)

    def patch_user_data(self, user_id, data, expected_status=None, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
            **kwargs,
        )

    def create_user(self, data, expected_status=None, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=f"{USER}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
            **kwargs,
        )

    def get_list_users(self, expected_status=None, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{USER}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )
