import pytest

from utils.api_client import get_brands_list, put_brands_list
from utils.assertions import assert_api_response

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_get_brands_list_returns_brands():
    body = assert_api_response(get_brands_list(), 200)

    assert isinstance(body["brands"], list)
    assert len(body["brands"]) > 0

    brand = body["brands"][0]
    assert "id" in brand
    assert "brand" in brand


@pytest.mark.negative
def test_put_brands_list_method_not_allowed():
    body = assert_api_response(put_brands_list(), 405)

    assert "not supported" in body["message"].lower()
