import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://automationexercise.com/api")
