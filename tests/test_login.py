import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from page_objects.login_page import LoginPage 
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
        
        # Use ChromeDriverManager with proper configuration for CI
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    else:
        # Local development settings
        options.add_argument("--window-size=1920,1080")
        
        # For local Mac, you might want to run with UI (remove headless)
        # Uncomment the next line if you want headless mode locally too
        # options.add_argument("--headless=new")
        
        if is_mac:
            # For Mac M1/M2 (ARM architecture), use the specific Chrome type
            try:
                # First attempt: Try with ChromeDriverManager
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                    options=options
                )
            except Exception as e:
                print(f"Failed with ChromeDriverManager: {e}")
                # Fallback: Try with system Chrome
                try:
                    driver = webdriver.Chrome(options=options)
                except Exception as e2:
                    print(f"Failed with system Chrome: {e2}")
                    # Last resort: Manual path (you'll need to update this path)
                    # Download ChromeDriver manually from https://chromedriver.chromium.org/
                    # and update the path below
                    chromedriver_path = "/usr/local/bin/chromedriver"  # Update this path
                    driver = webdriver.Chrome(
                        service=Service(chromedriver_path),
                        options=options
                    )
        else:
            # For other local systems (Windows, Linux)
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