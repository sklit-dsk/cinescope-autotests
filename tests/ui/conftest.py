import pytest
from playwright.sync_api import sync_playwright
from constants.ui_constants import UIConstants
from tools.trace import Tools
from models.ui_models import UIUserDemoQA, UIUserCinescope
from utils.data_generator import DataGenerator

@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    browser = playwright.chromium.launch(
        headless=True
    )  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()  # Браузер закрывается после завершения всех тестов


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


@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста


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
