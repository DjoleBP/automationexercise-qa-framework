import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.config import API_BASE_URL, REQUEST_RETRIES, REQUEST_TIMEOUT
from utils.data_factory import UserData

logger = logging.getLogger(__name__)

_SENSITIVE_KEYS = {"password"}


def _build_session() -> requests.Session:
    """One session for the whole run: connection reuse plus retries for transient errors.

    `allowed_methods` is left at urllib3's default idempotent set, which excludes POST --
    retrying `POST /createAccount` after a 5xx could create a second account and turn the
    retry into a confusing "Email already exists!" failure. Connection errors (where the
    request almost certainly never landed) are still retried for every method.
    """
    retry = Retry(
        total=REQUEST_RETRIES,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


session = _build_session()


def _redact(data: dict | None) -> dict | None:
    if not data:
        return data
    return {key: "***" if key in _SENSITIVE_KEYS else value for key, value in data.items()}


def _request(method: str, endpoint: str, data: dict | None = None) -> requests.Response:
    """Sends a form-encoded request and logs both sides of it.

    The logs are captured by pytest and printed for failing tests only, which is where
    the raw payload and response body are actually needed.
    """
    url = f"{API_BASE_URL}{endpoint}"
    logger.info("%s %s data=%s", method, url, _redact(data))

    response = session.request(method, url, data=data, timeout=REQUEST_TIMEOUT)

    logger.info("%s %s -> HTTP %s body=%s", method, url, response.status_code, response.text)
    return response


def create_account(user: UserData) -> requests.Response:
    payload = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "title": user.title,
        "birth_date": user.birth_day,
        "birth_month": user.birth_month,
        "birth_year": user.birth_year,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "company": user.company,
        "address1": user.address1,
        "address2": user.address2,
        "country": user.country,
        "zipcode": user.zipcode,
        "state": user.state,
        "city": user.city,
        "mobile_number": user.mobile_number,
    }
    return _request("POST", "/createAccount", payload)


def delete_account(email: str, password: str) -> requests.Response:
    return _request("DELETE", "/deleteAccount", {"email": email, "password": password})


def verify_login(email: str, password: str | None = None) -> requests.Response:
    payload = {"email": email}
    if password is not None:
        payload["password"] = password
    return _request("POST", "/verifyLogin", payload)


def get_products_list() -> requests.Response:
    return _request("GET", "/productsList")


def post_products_list() -> requests.Response:
    return _request("POST", "/productsList")


def get_brands_list() -> requests.Response:
    return _request("GET", "/brandsList")


def put_brands_list() -> requests.Response:
    return _request("PUT", "/brandsList")


def search_product(search_term: str | None) -> requests.Response:
    payload = {} if search_term is None else {"search_product": search_term}
    return _request("POST", "/searchProduct", payload)


def delete_verify_login() -> requests.Response:
    return _request("DELETE", "/verifyLogin")
