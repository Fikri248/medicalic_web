import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TEST_EMAIL = os.getenv("TEST_EMAIL", "fikri@admin")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "fikriadmin")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
