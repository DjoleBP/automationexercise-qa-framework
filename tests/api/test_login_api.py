import pytest

from utils.api_client import create_account, delete_account, delete_verify_login, verify_login
from utils.assertions import assert_api_response
from utils.data_factory import random_user

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_verify_login_with_valid_credentials():
    user = random_user()
    assert_api_response(create_account(user), 201)

    try:
        body = assert_api_response(verify_login(user.email, user.password), 200)
        assert body["message"] == "User exists!"
    finally:
        delete_account(user.email, user.password)


@pytest.mark.negative
def test_verify_login_with_invalid_credentials():
    response = verify_login("does_not_exist_qaframework@example.com", "WrongPassword123!")
    body = assert_api_response(response, 404)

    assert body["message"] == "User not found!"


@pytest.mark.negative
def test_verify_login_with_missing_password():
    body = assert_api_response(verify_login("someone@example.com"), 400)

    assert "missing" in body["message"].lower()


@pytest.mark.negative
def test_verify_login_delete_method_not_allowed():
    assert_api_response(delete_verify_login(), 405)
