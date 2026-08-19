import allure
import pytest
from playwright.sync_api import expect
from playwright.sync_api import Page
from utils.data_generator import DataGenerator

@allure.epic("Тестирование UI Cinescope")
@allure.feature("Создание отзыва")
@pytest.mark.ui
@pytest.mark.flaky
class TestReviews:
    @allure.step("Успешное создание и публикация отзыва")
    def test_create_review(
        self, page: Page, registered_and_login_user, movie_page, failure_screenshot
    ):
        with failure_screenshot():
            movie_page.open_film()
            movie_page.review(DataGenerator.generate_random_review())
            alert_create_review = page.get_by_role("status").filter(
                has_text="Отзыв успешно создан"
            )
            expect(alert_create_review).to_be_visible()
            assert False
