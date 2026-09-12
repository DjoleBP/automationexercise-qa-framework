import requests


def assert_api_response(response: requests.Response, expected_code: int) -> dict:
    """Asserts the response envelope and returns the parsed body for further checks.

    The site's API always answers HTTP 200; the real outcome lives in the JSON
    "responseCode" field, so both have to be checked on every call.
    """
    assert response.status_code == 200, (
        f"expected HTTP 200 from {response.url}, got {response.status_code}: {response.text}"
    )

    try:
        body = response.json()
    except ValueError:
        # An anti-bot interstitial answers HTTP 200 with an HTML challenge page, so the
        # status check above passes and it is response.json() that blows up. Say what
        # actually arrived rather than letting a bare JSONDecodeError surface.
        raise AssertionError(
            f"expected a JSON body from {response.url}, got "
            f"{response.headers.get('content-type', 'no content-type')}: {response.text[:500]}"
        ) from None

    assert body.get("responseCode") == expected_code, (
        f"expected responseCode {expected_code} from {response.url}, "
        f"got {body.get('responseCode')}: {response.text}"
    )
    return body
