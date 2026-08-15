import allure
from pages.base_page import BasePage
from playwright.sync_api import Page

class MoviePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}"
        self.show_more_button = '[data-qa-id="more_button"]'
        self.movie_review_input = '[data-qa-id="movie_review_input"]'
        self.movie_review_submit_button = '[data-qa-id="movie_review_submit_button"]'
        
    def open(self):
        self.open_url(self.url)
    
    @allure.step("Открытие страницы первого фильма на главной странице")
    def open_film(self):
        self.click(self.show_more_button)
    
    @allure.step("Заполнение поля отзыва и нажатие кнопки публикации отзыва")
    def review(self, review_text: str):
        self.page.wait_for_selector(self.movie_review_input)
        self.enter_text(self.movie_review_input, review_text)
        self.click(self.movie_review_submit_button)