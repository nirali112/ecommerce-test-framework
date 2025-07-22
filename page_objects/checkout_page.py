from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")
        self.checkout_button = (By.ID, "checkout")
        self.first_name_field = (By.ID, "first-name")
        self.last_name_field = (By.ID, "last-name")
        self.zip_field = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.success_message = (By.CLASS_NAME, "complete-header")

    def open_cart(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.cart_link)).click()

    def start_checkout(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.checkout_button)).click()

    def enter_checkout_info(self, first_name, last_name, zip_code):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.first_name_field)).send_keys(first_name)
        self.driver.find_element(*self.last_name_field).send_keys(last_name)
        self.driver.find_element(*self.zip_field).send_keys(zip_code)
        self.driver.find_element(*self.continue_button).click()

    def finish_checkout(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.finish_button)).click()

    def get_success_message(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located(self.success_message)).text
