from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "[data-test='error']")
        self.inventory_container = (By.CLASS_NAME, "inventory_container")

    @allure.step("Load login page")
    def load(self):
        self.driver.get("https://www.saucedemo.com/")
        allure.attach(
            self.driver.current_url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.step("Login with username: {username}")
    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)
        
        with allure.step(f"Enter username: {username}"):
            wait.until(EC.presence_of_element_located(self.username_field)).send_keys(username)
        
        with allure.step("Enter password"):
            # Don't log actual password for security
            wait.until(EC.presence_of_element_located(self.password_field)).send_keys(password)
        
        with allure.step("Click login button"):
            wait.until(EC.element_to_be_clickable(self.login_button)).click()
    
    @allure.step("Check if user is logged in")
    def is_logged_in(self):
        """Check if login was successful by looking for the inventory container"""
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located(self.inventory_container))
            return True
        except:
            return False
    
    @allure.step("Check if error message is displayed")
    def is_error_displayed(self):
        """Check if error message is displayed after failed login"""
        try:
            wait = WebDriverWait(self.driver, 5)
            error_element = wait.until(EC.presence_of_element_located(self.error_message))
            error_text = error_element.text
            allure.attach(
                error_text,
                name="Error Message",
                attachment_type=allure.attachment_type.TEXT
            )
            return True
        except:
            return False