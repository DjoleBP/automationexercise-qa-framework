import pytest

from utils.api_client import get_brands_list, put_brands_list

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_get_brands_list_returns_brands():
    response = get_brands_list()
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert isinstance(body["brands"], list)
    assert len(body["brands"]) > 0

    brand = body["brands"][0]
    assert "id" in brand
    assert "brand" in brand


@pytest.mark.negative
def test_put_brands_list_method_not_allowed():
    response = put_brands_list()
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
