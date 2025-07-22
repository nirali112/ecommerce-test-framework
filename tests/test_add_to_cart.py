import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from page_objects.products_page import ProductsPage
import platform
import os


def create_driver():
    """Creates a Chrome WebDriver instance compatible with both local and CI environments."""
    options = webdriver.ChromeOptions()
    
    # Detect if running on CI or local
    is_ci = os.environ.get('CI', 'false').lower() == 'true'
    is_mac = platform.system() == 'Darwin'
    
    if is_ci:
        # CI-specific settings (Linux GitHub Actions)
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    else:
        # Local development settings
        options.add_argument("--window-size=1920,1080")
        
        if is_mac:
            try:
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                    options=options
                )
            except Exception as e:
                print(f"Failed with ChromeDriverManager: {e}")
                try:
                    driver = webdriver.Chrome(options=options)
                except Exception as e2:
                    print(f"Failed with system Chrome: {e2}")
                    chromedriver_path = "/usr/local/bin/chromedriver"
                    driver = webdriver.Chrome(
                        service=Service(chromedriver_path),
                        options=options
                    )
        else:
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

def test_add_item_to_cart(driver):
    products_page = ProductsPage(driver)
    products_page.load()
    products_page.add_item_to_cart("Sauce Labs Backpack")
    assert products_page.is_item_in_cart("Sauce Labs Backpack")
