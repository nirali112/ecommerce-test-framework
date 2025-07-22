from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "[data-test='error']")
        self.inventory_container = (By.CLASS_NAME, "inventory_container")

    def load(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)  # wait up to 10s for elements
        wait.until(EC.presence_of_element_located(self.username_field)).send_keys(username)
        wait.until(EC.presence_of_element_located(self.password_field)).send_keys(password)
        wait.until(EC.element_to_be_clickable(self.login_button)).click()
    
    def is_logged_in(self):
        """Check if login was successful by looking for the inventory container"""
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located(self.inventory_container))
            return True
        except:
            return False
    
    def is_error_displayed(self):
        """Check if error message is displayed after failed login"""
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located(self.error_message))
            return True
        except:
            return False