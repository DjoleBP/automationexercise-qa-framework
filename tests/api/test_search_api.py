import pytest

from utils.api_client import search_product
from utils.assertions import assert_api_response

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_search_product_with_valid_term_returns_matches():
    body = assert_api_response(search_product("top"), 200)

    assert len(body["products"]) > 0

    # The search matches on category as well as product name (e.g. a "Tops & Shirts"
    # category item can match "top" even without "top" in its own name) -- verified
    # against the live API rather than assumed.
    def matches(product):
        haystack = f"{product['name']} {product['category']['category']}".lower()
        return "top" in haystack

    assert all(matches(product) for product in body["products"])


@pytest.mark.negative
def test_search_product_with_missing_parameter():
    body = assert_api_response(search_product(None), 400)

    assert "search_product parameter is missing" in body["message"]


@pytest.mark.negative
def test_search_product_with_no_matching_term_returns_empty_list():
    body = assert_api_response(search_product("zzznonexistentproductxyz"), 200)

    assert body["products"] == []
