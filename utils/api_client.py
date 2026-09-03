import requests

from utils.config import API_BASE_URL
from utils.data_factory import UserData


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
    return requests.post(f"{API_BASE_URL}/createAccount", data=payload)


def delete_account(email: str, password: str) -> requests.Response:
    return requests.delete(f"{API_BASE_URL}/deleteAccount", data={"email": email, "password": password})


def verify_login(email: str, password: str | None = None) -> requests.Response:
    payload = {"email": email}
    if password is not None:
        payload["password"] = password
    return requests.post(f"{API_BASE_URL}/verifyLogin", data=payload)


def get_products_list() -> requests.Response:
    return requests.get(f"{API_BASE_URL}/productsList")


def post_products_list() -> requests.Response:
    return requests.post(f"{API_BASE_URL}/productsList")


def get_brands_list() -> requests.Response:
    return requests.get(f"{API_BASE_URL}/brandsList")


def put_brands_list() -> requests.Response:
    return requests.put(f"{API_BASE_URL}/brandsList")


def search_product(search_term: str | None) -> requests.Response:
    payload = {} if search_term is None else {"search_product": search_term}
    return requests.post(f"{API_BASE_URL}/searchProduct", data=payload)


def delete_verify_login() -> requests.Response:
    return requests.delete(f"{API_BASE_URL}/verifyLogin")
