import pytest
import os
from selenium import webdriver
from config import HEADLESS, DOWNLOAD_DIR

@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()

    # Suppress Chrome internal logs (TensorFlow Lite, GCM errors, etc.)
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if HEADLESS:
        options.add_argument("--headless=new")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    prefs = {
        "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver

    driver.quit()