from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from page_objects.login_page import LoginPage
import time
from webdriver_manager.chrome import ChromeDriverManager


# class TestLogin:
def test_valid_login():
    # Setup driver (using manually installed chromedriver)
    service = Service("/usr/local/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(service=service, options=options)
    # self.driver = webdriver.Chrome(service=service, options=options)  # store driver in self

    # Create page object
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    # login_page.login("wrong_user", "wrong_pass")

    # Wait just to see the page after login
    # time.sleep(10)

    # Assert login success
    assert "Products" in driver.page_source

    driver.quit()
