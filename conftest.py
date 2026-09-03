import pytest

from utils.api_client import create_account, delete_account
from utils.data_factory import UserData, random_user


@pytest.fixture
def registered_user() -> UserData:
    """Provisions a throwaway account via the API (fast, independent of UI) and deletes it after the test."""
    user = random_user()
    response = create_account(user)
    # The API always answers HTTP 200; the real result lives in the "responseCode" field.
    assert response.json().get("responseCode") == 201, f"createAccount failed: {response.text}"

    yield user

    delete_account(user.email, user.password)
