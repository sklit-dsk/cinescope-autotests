import pytest
from playwright.sync_api import sync_playwright
from constants.ui_constants import UIConstants
from tools.trace import Tools
from models.ui_models import UIUserDemoQA, UIUserCinescope
from utils.data_generator import DataGenerator
from playwright.sync_api import Page
from pages.register_page import CinescopeRegisterPage
from pages.login_page import CinescopeLoginPage
from pages.movie_page import MoviePage
from playwright.sync_api import expect

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(UIConstants.DEFAULT_UI_TIMEOUT.value)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir("playwright_trace", log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def register_page(page: Page) -> CinescopeRegisterPage:
    register_page = CinescopeRegisterPage(page)
    register_page.open()
    return register_page


@pytest.fixture
def login_page(page: Page) -> CinescopeLoginPage:
    login_page = CinescopeLoginPage(page)
    login_page.open()
    return login_page


@pytest.fixture
def movie_page(page: Page) -> MoviePage:
    movie_page = MoviePage(page)
    movie_page.open()
    return movie_page


@pytest.fixture
def registered_and_login_user(
    page: Page, login_page, register_page, ui_user_data_cinescope
):
    register_page.register(
        ui_user_data_cinescope.userName,
        ui_user_data_cinescope.userEmail,
        ui_user_data_cinescope.password,
    )
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()
    login_page.login(ui_user_data_cinescope.userEmail, ui_user_data_cinescope.password)
    alert_before_login = page.get_by_role("status").filter(
        has_text="Что-то пошло не так"
    )
    expect(alert_before_login).to_be_visible()
    page.reload()


@pytest.fixture(scope="function")
def ui_user_data() -> UIUserDemoQA:
    return UIUserDemoQA(
        userName=DataGenerator.generate_random_name(),
        firstName=DataGenerator.generate_firstname(),
        lastName=DataGenerator.generate_lastname(),
        userEmail=DataGenerator.generate_random_email(),
        userAge=DataGenerator.generate_age(),
        userSalary=DataGenerator.generate_salary(),
        userDepartament=DataGenerator.generate_departament(),
        userPhoneNumber=DataGenerator.generate_mobile_number(),
        password=DataGenerator.generate_random_password(),
    )


@pytest.fixture(scope="function")
def ui_user_data_cinescope() -> UIUserCinescope:
    return UIUserCinescope(
        userName=DataGenerator.generate_random_name(),
        userEmail=DataGenerator.generate_random_email(),
        password=DataGenerator.generate_random_password(),
    )
