from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        # Login elements
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        # Product elements
        self.add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")
        # Cart and checkout elements
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")
        self.checkout_button = (By.ID, "checkout")
        self.first_name_field = (By.ID, "first-name")
        self.last_name_field = (By.ID, "last-name")
        self.zip_field = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.success_message = (By.CLASS_NAME, "complete-header")

    def load(self):
        """Load the page and prepare for checkout by logging in and adding an item"""
        self.driver.get("https://www.saucedemo.com/")
        # Login
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.username_field)).send_keys("standard_user")
        self.driver.find_element(*self.password_field).send_keys("secret_sauce")
        self.driver.find_element(*self.login_button).click()
        # Add an item to cart
        wait.until(EC.element_to_be_clickable(self.add_to_cart_button)).click()
        time.sleep(1)

    def perform_checkout(self, first_name, last_name, zip_code):
        """Complete the entire checkout process"""
        wait = WebDriverWait(self.driver, 10)
        
        # First, we need to go to the cart page
        # The cart link should be visible after adding an item
        wait.until(EC.element_to_be_clickable(self.cart_link)).click()
        
        # Wait for cart page to load and click checkout
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))
        wait.until(EC.element_to_be_clickable(self.checkout_button)).click()
        
        # Enter checkout information
        wait.until(EC.presence_of_element_located(self.first_name_field)).send_keys(first_name)
        self.driver.find_element(*self.last_name_field).send_keys(last_name)
        self.driver.find_element(*self.zip_field).send_keys(zip_code)
        self.driver.find_element(*self.continue_button).click()
        
        # Finish checkout
        wait.until(EC.element_to_be_clickable(self.finish_button)).click()


    def is_order_successful(self):
        """Check if order was completed successfully"""
        try:
            wait = WebDriverWait(self.driver, 10)
            success_element = wait.until(EC.presence_of_element_located(self.success_message))
            return success_element.text == "Thank you for your order!"
        except:
            return False

    def get_success_message(self):
        """Get the success message text"""
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located(self.success_message)).text