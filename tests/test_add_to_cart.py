import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from page_objects.products_page import ProductsPage  # adjust import if needed

def create_driver():
    """Creates a Chrome WebDriver instance compatible with GitHub Actions CI."""
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"  # needed for CI

    # CI-friendly options
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

def test_add_item_to_cart(driver):
    products_page = ProductsPage(driver)
    products_page.load()
    products_page.add_item_to_cart("Sauce Labs Backpack")
    assert products_page.is_item_in_cart("Sauce Labs Backpack")
