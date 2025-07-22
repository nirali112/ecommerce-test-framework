from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from page_objects.login_page import LoginPage
from page_objects.products_page import ProductsPage
from page_objects.checkout_page import CheckoutPage
import time
from webdriver_manager.chrome import ChromeDriverManager

# class TestCheckoutFlow:
def test_checkout_flow():
    service = Service("/usr/local/bin/chromedriver")
    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_argument("--headless=new")     # Needed for GitHub CI
    options.add_argument("--no-sandbox")       # Needed for Linux CI
    options.add_argument("--disable-dev-shm-usage")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)    # driver = webdriver.Chrome(service=service, options=options)
    # self.driver = webdriver.Chrome(service=service, options=options)  # store driver in self

    # Step 1: Login
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    # Step 2: Add product to cart
    products_page = ProductsPage(driver)
    products_page.add_item_to_cart()

    # Step 3: Go to checkout
    checkout_page = CheckoutPage(driver)
    checkout_page.open_cart()
    checkout_page.start_checkout()

    # Step 4: Enter checkout info
    checkout_page.enter_checkout_info("Nirali", "Mehta", "12345")

    # Step 5: Finish checkout
    checkout_page.finish_checkout()

    # Step 6: Verify success message
    success_message = checkout_page.get_success_message()
    assert success_message == "Thank you for your order!"
    time.sleep(120)
    driver.quit()
