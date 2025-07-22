from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from page_objects.login_page import LoginPage
from page_objects.products_page import ProductsPage
import time
from webdriver_manager.chrome import ChromeDriverManager

# class TestAddToCart:
def test_add_item_to_cart():
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

    # Step 3: Verify cart count
    cart_count = products_page.get_cart_count()
    assert cart_count == "1"  # Expecting 1 item in cart

    time.sleep(60)
    driver.quit()