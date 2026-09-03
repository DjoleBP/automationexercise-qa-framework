import uuid
from dataclasses import dataclass, field

from faker import Faker

fake = Faker()


@dataclass
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


def unique_email(prefix: str = "qaframework") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}@mailinator.com"


def random_user(prefix: str = "qaframework") -> UserData:
    return UserData(
        name=fake.name(),
        email=unique_email(prefix),
        password=fake.password(length=12),
        title=fake.random_element(elements=("Mr", "Mrs")),
        birth_day=str(fake.random_int(min=1, max=28)),
        birth_month=str(fake.random_int(min=1, max=12)),
        birth_year=str(fake.random_int(min=1970, max=2005)),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        company=fake.company(),
        address1=fake.street_address(),
        address2=fake.secondary_address(),
        country="Canada",
        state=fake.state(),
        city=fake.city(),
        zipcode=fake.postcode(),
        mobile_number=fake.numerify("##########"),
    )


@dataclass
class ContactMessage:
    name: str = field(default_factory=fake.name)
    email: str = field(default_factory=lambda: unique_email("contact"))
    subject: str = field(default_factory=lambda: fake.sentence(nb_words=4))
    message: str = field(default_factory=lambda: fake.paragraph(nb_sentences=3))
