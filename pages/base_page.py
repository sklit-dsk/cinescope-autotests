import allure

from pages.actions import PageAction
from constants.base_urls import BASE_PAGE


class BasePage(PageAction):
    def __init__(self, page):
        super().__init__(page)
        self.home_url = BASE_PAGE
        self.all_movies_link = 'a[href="/movies"]'

    @allure.step("Переход на 'Все фильмы' из шапки")
    def go_to_all_movies(self):
        self.click(self.all_movies_link)
