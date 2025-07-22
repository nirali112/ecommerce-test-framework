import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page_objects import LoginPage  # adjust import if needed


def create_driver():
    """Creates a Chrome WebDriver instance compatible with GitHub Actions CI."""
    options = webdriver.ChromeOptions()

    # Explicitly set Chrome binary for CI (GitHub runners)
    options.binary_location = "/usr/bin/google-chrome"

    # Required flags for running in CI environments
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Use webdriver-manager to get the correct ChromeDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()


def test_invalid_login(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("invalid_user", "wrong_password")
    assert login_page.is_error_displayed()
