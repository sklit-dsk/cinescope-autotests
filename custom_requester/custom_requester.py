import json
import logging
import os
import allure
from typing import Any
from requests import Response, Session
from requests.structures import CaseInsensitiveDict
from models.base_models import BaseModel
from constants.colors import Colors

class CustomRequester:
    with allure.step("Установка заголовков"):
        base_headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def __init__(self, session: Session, base_url: str) -> None:
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.session.headers.update(self.base_headers)
        self.logger = logging.getLogger(__name__)

    def send_request(
        self,
        method: str,
        endpoint: str,
        data: Any = None,
        params: Any = None,
        expected_status: int | None = 201,
        need_logging: bool = False,
        **kwargs: Any,
    ) -> Response:
        with allure.step("Формирование запроса через кастомный реквестер"):
            url = f"{self.base_url}{endpoint}"
            with allure.step("Проверка входных данных запроса"):
                if isinstance(data, BaseModel):
                    data = json.loads(data.model_dump_json(exclude_unset=True))

            with allure.step("Отправка запроса по входным параметрам"):
                response = self.session.request(
                    method, url, json=data, params=params, **kwargs
                )

            if need_logging:
                self.log_request_and_response(response)

            if expected_status is not None and response.status_code != expected_status:
                raise ValueError(
                    f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
                )

            return response

    def _update_session_headers(self, headers: dict[str, str]) -> None:
        with allure.step("Обновление заговков"):
            self.session.headers.update(headers)

    def _reset_headers(self, headers: dict[str, str]) -> None:
        with allure.step("Сброс заголовков"):
            self.session.headers = CaseInsensitiveDict(self.base_headers)
            self.session.headers.update(headers)

    def log_request_and_response(self, response: Response) -> None:
        try:
            request = response.request
            header_lines = []
            for header, value in request.headers.items():
                header_value = (
                    value.decode("utf-8") if isinstance(value, bytes) else value
                )
                header_lines.append(f"-H '{header}: {header_value}'")
            headers = " \\\n".join(header_lines)
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, "body") and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode("utf-8")
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != "{}" else ""

            self.logger.info(
                f"{Colors.GREEN}{full_test_name}{Colors.RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(
                    f"\tRESPONSE:"
                    f"\nSTATUS_CODE: {Colors.RED}{response_status}{Colors.RESET}"
                    f"\nDATA: {Colors.RED}{response_data}{Colors.RESET}"
                )
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
