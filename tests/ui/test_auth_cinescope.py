from playwright.sync_api import Page, expect
from constants.base_urls import CINESCOPE_UI_REGISTER
from models.ui_models import UIUserCinescope


def test_registration(page: Page, ui_user_data_cinescope: UIUserCinescope):
    page.goto(CINESCOPE_UI_REGISTER)
    username_locator = '[data-qa-id="register_full_name_input"]'
    email_locator = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'
    page.fill(username_locator, ui_user_data_cinescope.userName)
    page.fill(email_locator, f"{ui_user_data_cinescope.userEmail}")
    page.fill(password_locator, f"{ui_user_data_cinescope.password}")
    page.fill(repeat_password_locator, f"{ui_user_data_cinescope.password}")
    page.click('[data-qa-id="register_submit_button"]')
    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
