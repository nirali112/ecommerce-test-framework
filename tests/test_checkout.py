import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from page_objects.checkout_page import CheckoutPage  # adjust import if needed

def create_driver():
    """Creates a Chrome WebDriver instance compatible with GitHub Actions CI."""
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()

def test_checkout_flow(driver):
    checkout_page = CheckoutPage(driver)
    checkout_page.load()
    checkout_page.perform_checkout("John", "Doe", "12345")
    assert checkout_page.is_order_successful()
