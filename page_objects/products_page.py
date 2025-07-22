from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    def add_item_to_cart(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.add_to_cart_button)).click()

    def get_cart_count(self):
        wait = WebDriverWait(self.driver, 10)
        badge = wait.until(EC.presence_of_element_located(self.cart_badge))
        return badge.text
