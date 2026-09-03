import pytest

from utils.api_client import get_products_list, post_products_list

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_get_products_list_returns_products():
    response = get_products_list()
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0

    product = body["products"][0]
    for field in ("id", "name", "price", "brand", "category"):
        assert field in product
    assert "usertype" in product["category"]
    assert "category" in product["category"]


@pytest.mark.negative
def test_post_products_list_method_not_allowed():
    response = post_products_list()
    body = response.json()

    # The API always answers HTTP 200; the real result lives in "responseCode".
    assert response.status_code == 200
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
