from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')
    username_locator = '[data-qa-id="register_full_name_input"]'
    email_locator = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    password = DataGenerator.generate_random_password()

    page.fill(username_locator, DataGenerator.generate_random_name())
    page.fill(email_locator, f'{DataGenerator.generate_random_email()}')
    page.fill(password_locator, f'{password}')
    page.fill(repeat_password_locator, f'{password}')
    page.click('[data-qa-id="register_submit_button"]')
    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

