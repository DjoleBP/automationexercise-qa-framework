import pytest

from utils.api_client import create_account, delete_account
from utils.assertions import assert_api_response
from utils.data_factory import random_user

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_create_and_delete_account():
    user = random_user()

    create_body = assert_api_response(create_account(user), 201)
    assert create_body["message"] == "User created!"

    delete_body = assert_api_response(delete_account(user.email, user.password), 200)
    assert delete_body["message"] == "Account deleted!"


@pytest.mark.negative
def test_create_account_with_already_registered_email():
    user = random_user()
    create_account(user)

    try:
        duplicate_body = assert_api_response(create_account(user), 400)
        assert duplicate_body["message"] == "Email already exists!"
    finally:
        delete_account(user.email, user.password)
