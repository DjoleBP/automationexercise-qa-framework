import pytest

from utils.api_client import create_account, delete_account, delete_verify_login, verify_login
from utils.data_factory import random_user

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_verify_login_with_valid_credentials():
    user = random_user()
    create_response = create_account(user)
    assert create_response.json()["responseCode"] == 201

    try:
        response = verify_login(user.email, user.password)
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 200
        assert body["message"] == "User exists!"
    finally:
        delete_account(user.email, user.password)


@pytest.mark.negative
def test_verify_login_with_invalid_credentials():
    response = verify_login("does_not_exist_qaframework@example.com", "WrongPassword123!")
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 404
    assert body["message"] == "User not found!"


@pytest.mark.negative
def test_verify_login_with_missing_password():
    response = verify_login("someone@example.com")
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 400
    assert "missing" in body["message"].lower()


@pytest.mark.negative
def test_verify_login_delete_method_not_allowed():
    response = delete_verify_login()
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 405
