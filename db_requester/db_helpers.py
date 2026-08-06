import allure
from typing import Any
from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movies import MovieDBModel


class DBHelper:

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    with allure.step("Создание тестового пользователя в БД"):

        def create_test_user(self, user_data: UserDBModel) -> UserDBModel:
            self.db_session.add(user_data)
            self.db_session.commit()
            self.db_session.refresh(user_data)
            return user_data

    with allure.step("Получение пользователя по id из БД"):

        def get_user_by_id(self, user_id: object) -> UserDBModel | None:
            return (
                self.db_session.query(UserDBModel)
                .filter(UserDBModel.id == user_id)
                .first()
            )

    with allure.step("Получение пользователя по email из БД"):

        def get_user_by_email(self, email: str) -> UserDBModel | None:
            return (
                self.db_session.query(UserDBModel)
                .filter(UserDBModel.email == email)
                .first()
            )

    with allure.step("Получение фильма по названию из БД"):

        def get_movie_by_name(self, name: str) -> MovieDBModel | None:
            return (
                self.db_session.query(MovieDBModel)
                .filter(MovieDBModel.name == name)
                .first()
            )

    with allure.step("Проверка существования пользователя в БД по email"):

        def user_exists_by_email(self, email: str) -> bool:
            return (
                self.db_session.query(UserDBModel)
                .filter(UserDBModel.email == email)
                .count()
                > 0
            )

    with allure.step("Удаление пользователя по id из БД"):

        def delete_user(self, user: UserDBModel) -> None:
            self.db_session.delete(user)
            self.db_session.commit()

    with allure.step("Очистка тестовых данных в БД"):

        def cleanup_test_data(self, objects_to_delete: list[Any]) -> None:

            for obj in objects_to_delete:
                if obj:
                    self.db_session.delete(obj)
            self.db_session.commit()

    with allure.step("Получение фильма по id из БД"):

        def get_movie_by_id(self, movie_id: int) -> MovieDBModel | None:
            """Получает фильм по ID"""
            return (
                self.db_session.query(MovieDBModel)
                .filter(MovieDBModel.id == movie_id)
                .first()
            )
