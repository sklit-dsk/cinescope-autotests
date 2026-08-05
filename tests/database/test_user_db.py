from db_models.user import UserDBModel
from db_requester.db_helpers import DBHelper
from pytest_check import check


def test_db_requests(db_helper: DBHelper, created_test_user: UserDBModel):
    with check:
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")
