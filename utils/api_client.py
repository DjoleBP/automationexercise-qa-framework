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


def verify_login(email: str, password: str) -> requests.Response:
    return requests.post(f"{API_BASE_URL}/verifyLogin", data={"email": email, "password": password})
