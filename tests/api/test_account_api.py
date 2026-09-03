import pytest

from utils.api_client import create_account, delete_account
from utils.data_factory import random_user

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_create_and_delete_account():
    user = random_user()

    create_response = create_account(user)
    create_body = create_response.json()
    assert create_response.status_code == 200
    assert create_body["responseCode"] == 201
    assert create_body["message"] == "User created!"

    delete_response = delete_account(user.email, user.password)
    delete_body = delete_response.json()
    assert delete_response.status_code == 200
    assert delete_body["responseCode"] == 200
    assert delete_body["message"] == "Account deleted!"


@pytest.mark.negative
def test_create_account_with_already_registered_email():
    user = random_user()
    create_account(user)

    try:
        duplicate_response = create_account(user)
        duplicate_body = duplicate_response.json()

        assert duplicate_response.status_code == 200
        assert duplicate_body["responseCode"] == 400
        assert duplicate_body["message"] == "Email already exists!"
    finally:
        delete_account(user.email, user.password)
