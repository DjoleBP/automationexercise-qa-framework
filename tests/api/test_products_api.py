import pytest

from utils.api_client import get_products_list, post_products_list
from utils.assertions import assert_api_response

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_get_products_list_returns_products():
    body = assert_api_response(get_products_list(), 200)

    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0

    product = body["products"][0]
    for field in ("id", "name", "price", "brand", "category"):
        assert field in product
    assert "usertype" in product["category"]
    assert "category" in product["category"]


@pytest.mark.negative
def test_post_products_list_method_not_allowed():
    body = assert_api_response(post_products_list(), 405)

    assert "not supported" in body["message"].lower()
