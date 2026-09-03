import pytest

from utils.api_client import search_product

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_search_product_with_valid_term_returns_matches():
    response = search_product("top")
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
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
    response = search_product(None)
    body = response.json()

    # The API always answers HTTP 200; the real result lives in "responseCode".
    assert response.status_code == 200
    assert body["responseCode"] == 400
    assert "search_product parameter is missing" in body["message"]


@pytest.mark.negative
def test_search_product_with_no_matching_term_returns_empty_list():
    response = search_product("zzznonexistentproductxyz")
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert body["products"] == []
