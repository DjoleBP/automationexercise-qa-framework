import logging
import uuid
from dataclasses import dataclass

from faker import Faker

from utils.config import FAKER_SEED

logger = logging.getLogger(__name__)

fake = Faker()

if FAKER_SEED is not None:
    Faker.seed(int(FAKER_SEED))
    logger.info("Faker seeded with FAKER_SEED=%s -- data repeats, except emails", FAKER_SEED)

# The signup form's country field is a <select> with a fixed list, so anything outside
# it would fail select_option(). State is a free-text input, but it is generated from
# the matching province list to keep the address internally consistent.
COUNTRY = "Canada"
CANADIAN_PROVINCES = (
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
)


@dataclass(frozen=True)
class UserData:
    name: str
    email: str
    password: str
    title: str
    birth_day: str
    birth_month: str
    birth_year: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str


@dataclass(frozen=True)
class ContactMessage:
    name: str
    email: str
    subject: str
    message: str


def unique_email(prefix: str = "qaframework") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}@mailinator.com"


def random_user(prefix: str = "qaframework", **overrides) -> UserData:
    """A fresh user with a unique email.

    Pass keyword overrides to pin individual fields, e.g. `random_user(email="not-an-email")`
    for a negative test that needs everything valid except one value.
    """
    defaults = {
        "name": fake.name(),
        "email": unique_email(prefix),
        "password": fake.password(length=12),
        # Only these two exist as radio buttons on the signup form.
        "title": fake.random_element(elements=("Mr", "Mrs")),
        # Capped at 28 so the day is valid in every month, February included.
        "birth_day": str(fake.random_int(min=1, max=28)),
        "birth_month": str(fake.random_int(min=1, max=12)),
        # Must exist as an option in the form's year dropdown.
        "birth_year": str(fake.random_int(min=1970, max=2005)),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": fake.secondary_address(),
        "country": COUNTRY,
        "state": fake.random_element(elements=CANADIAN_PROVINCES),
        "city": fake.city(),
        "zipcode": fake.postcode(),
        # Ten bare digits: phone_number() would add punctuation and an extension.
        "mobile_number": fake.numerify("##########"),
    }
    return UserData(**{**defaults, **overrides})


def random_contact_message(prefix: str = "contact", **overrides) -> ContactMessage:
    """A fresh contact-form message. Accepts the same keyword overrides as `random_user`."""
    defaults = {
        "name": fake.name(),
        "email": unique_email(prefix),
        "subject": fake.sentence(nb_words=4),
        "message": fake.paragraph(nb_sentences=3),
    }
    return ContactMessage(**{**defaults, **overrides})
