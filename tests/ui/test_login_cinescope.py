import allure
import pytest
import time
from playwright.sync_api import expect
from playwright.sync_api import Page


@allure.epic("Тестирование UI Cinescope")
@allure.feature("Логин")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешный логин зарегестрированного пользователя")
    def test_login(
        self,
        login_page,
        page: Page,
        ui_user_data_cinescope,
        register_page,
    ):
        register_page.register(ui_user_data_cinescope.userName, ui_user_data_cinescope.userEmail, ui_user_data_cinescope.password)
        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()
        login_page.login(
            ui_user_data_cinescope.userEmail, ui_user_data_cinescope.password
        )
        alert_before_login = page.get_by_role("status").filter(
            has_text="Вы вошли в аккаунт"
        )
        expect(alert_before_login).to_be_visible()
        assert False
