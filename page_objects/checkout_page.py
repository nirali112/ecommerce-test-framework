from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
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

    @allure.step("Load checkout page and prepare cart")
    def load(self):
        """Load the page and prepare for checkout by logging in and adding an item"""
        with allure.step("Navigate to SauceDemo website"):
            self.driver.get("https://www.saucedemo.com/")
            
        with allure.step("Login as standard user"):
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(self.username_field)).send_keys("standard_user")
            self.driver.find_element(*self.password_field).send_keys("secret_sauce")
            self.driver.find_element(*self.login_button).click()
            
        with allure.step("Wait for inventory page to load"):
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_container")))
            time.sleep(1)  # Ensure page is fully loaded
            
        with allure.step("Add Sauce Labs Backpack to cart"):
            # Wait for button and scroll into view
            add_button = wait.until(EC.element_to_be_clickable(self.add_to_cart_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(0.5)
            add_button.click()
            
            # Wait for cart badge to appear
            time.sleep(2)
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Product added to cart",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.step("Perform checkout with customer info - {first_name} {last_name}")
    def perform_checkout(self, first_name, last_name, zip_code):
        """Complete the entire checkout process"""
        wait = WebDriverWait(self.driver, 10)
        
        with allure.step("Navigate to shopping cart"):
            cart_button = wait.until(EC.element_to_be_clickable(self.cart_link))
            cart_button.click()
            
            # Wait for cart page - just wait a bit for page transition
            time.sleep(1)
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Shopping cart view",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Click checkout button"):
            # The checkout button should be visible now
            checkout_btn = wait.until(EC.element_to_be_clickable(self.checkout_button))
            checkout_btn.click()
            
            # Wait for checkout form
            time.sleep(1)
        
        with allure.step(f"Fill checkout information: {first_name} {last_name}, ZIP: {zip_code}"):
            # Enter checkout information
            wait.until(EC.presence_of_element_located(self.first_name_field)).send_keys(first_name)
            self.driver.find_element(*self.last_name_field).send_keys(last_name)
            self.driver.find_element(*self.zip_field).send_keys(zip_code)
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Checkout information filled",
                attachment_type=allure.attachment_type.PNG
            )
            
            self.driver.find_element(*self.continue_button).click()
        
        with allure.step("Complete order"):
            # Wait for overview page
            time.sleep(1)
            finish_btn = wait.until(EC.element_to_be_clickable(self.finish_button))
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Order overview",
                attachment_type=allure.attachment_type.PNG
            )
            
            finish_btn.click()

    @allure.step("Verify order completion")
    def is_order_successful(self):
        """Check if order was completed successfully"""
        try:
            wait = WebDriverWait(self.driver, 10)
            success_element = wait.until(EC.presence_of_element_located(self.success_message))
            success_text = success_element.text
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Order confirmation page",
                attachment_type=allure.attachment_type.PNG
            )
            
            return success_text == "Thank you for your order!"
        except Exception as e:
            allure.attach(
                str(e),
                name="Order verification error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    @allure.step("Get order success message")
    def get_success_message(self):
        """Get the success message text"""
        wait = WebDriverWait(self.driver, 10)
        message_element = wait.until(EC.presence_of_element_located(self.success_message))
        message = message_element.text
        
        allure.attach(
            message,
            name="Order success message",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return message