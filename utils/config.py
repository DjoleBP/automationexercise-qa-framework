import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://automationexercise.com/api")

# Seconds to wait for the API before giving up. Without an explicit timeout `requests`
# waits forever, which hangs a CI job instead of failing the test.
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))

# Retries for transient failures against the public site (connection errors and 5xx).
REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "2"))

# Set FAKER_SEED to replay a previous run's Faker-generated data, e.g. to reproduce a CI
# failure locally. Emails are deliberately excluded -- they come from uuid4, so they stay
# unique even on a seeded replay (a repeated email would just fail as already registered).
# Unset means fresh random data every run, which is the normal mode.
FAKER_SEED = os.getenv("FAKER_SEED")
