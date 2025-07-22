from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def load(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)  # wait up to 10s for elements
        wait.until(EC.presence_of_element_located(self.username_field)).send_keys(username)
        wait.until(EC.presence_of_element_located(self.password_field)).send_keys(password)
        wait.until(EC.element_to_be_clickable(self.login_button)).click()
