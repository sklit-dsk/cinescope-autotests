import allure
import pytest
from playwright.sync_api import expect
from playwright.sync_api import Page
import time

@allure.epic("Тестирование UI")
@allure.feature("Логин")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешный логин зарегестрированного пользователя")
    def test_login(self, login_page, page: Page, ui_user_data_cinescope, register_page):
        register_page.register(ui_user_data_cinescope.userName, ui_user_data_cinescope.userEmail, ui_user_data_cinescope.password)
        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()
        login_page.login(ui_user_data_cinescope.userEmail, ui_user_data_cinescope.userEmail)
        expect(page.get_by_role("button", name="Войти")).to_be_disabled()