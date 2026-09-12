import requests


def assert_api_response(response: requests.Response, expected_code: int) -> dict:
    """Asserts the response envelope and returns the parsed body for further checks.

    The site's API always answers HTTP 200; the real outcome lives in the JSON
    "responseCode" field, so both have to be checked on every call.
    """
    assert response.status_code == 200, (
        f"expected HTTP 200 from {response.url}, got {response.status_code}: {response.text}"
    )

    body = response.json()
    assert body.get("responseCode") == expected_code, (
        f"expected responseCode {expected_code} from {response.url}, "
        f"got {body.get('responseCode')}: {response.text}"
    )
    return body
