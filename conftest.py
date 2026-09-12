import pytest

from utils.api_client import create_account, delete_account
from utils.assertions import assert_api_response
from utils.data_factory import UserData, random_user


@pytest.fixture
def registered_user() -> UserData:
    """Provisions a throwaway account via the API (fast, independent of UI) and deletes it after the test."""
    user = random_user()
    assert_api_response(create_account(user), 201)

    yield user

    delete_account(user.email, user.password)
