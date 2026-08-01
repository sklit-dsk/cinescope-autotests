from typing import Any
from requests import Response, Session
from custom_requester.custom_requester import CustomRequester
from constants.base_urls import AUTH_BASE_URL

USER = '/user'


class UserApi(CustomRequester):

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def get_user_info(self, user_id: str, expected_status: int | None = None) -> Response:
        return self.send_request(
            method="GET",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    def delete_user(self, user_id: str, expected_status: int = 200) -> Response:
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            need_logging=True,
        )

    def patch_user_data(
        self,
        user_id: str,
        data: dict[str, object],
        expected_status: int | None = None,
    ) -> Response:
        return self.send_request(
            method="PATCH",
            endpoint=f"{USER}/{user_id}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
        )

    def create_user(
        self,
        data: Any,
        expected_status: int = 201,
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=f"{USER}",
            expected_status=expected_status,
            data=data,
            need_logging=True,
        )

    def get_list_users(self, expected_status: int | None = None, **kwargs) -> Response:
        return self.send_request(
            method="GET",
            endpoint=f"{USER}",
            expected_status=expected_status,
            need_logging=True,
            **kwargs,
        )
