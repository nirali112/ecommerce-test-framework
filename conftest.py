import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import platform
import os
from datetime import datetime


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
def driver(request):
    """WebDriver fixture with automatic screenshot on failure"""
    with allure.step("Initialize WebDriver"):
        driver = create_driver()
        driver.implicitly_wait(10)
    
    yield driver
    
    # Capture screenshot on test failure
    if request.node.rep_call.failed:
        try:
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"screenshot_{request.node.name}_{timestamp}.png"
            
            # Attach screenshot to Allure report
            allure.attach(
                driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )
            
            # Attach page source
            allure.attach(
                driver.page_source,
                name=f"page_source_{timestamp}.html",
                attachment_type=allure.attachment_type.HTML
            )
            
            # Attach browser logs
            logs = driver.get_log("browser")
            if logs:
                log_content = "\n".join([f"{log['level']}: {log['message']}" for log in logs])
                allure.attach(
                    log_content,
                    name=f"browser_logs_{timestamp}.txt",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")
    
    with allure.step("Quit WebDriver"):
        driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot functionality"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)