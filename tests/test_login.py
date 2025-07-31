import pytest
import allure
from page_objects.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("User Login")
class TestLogin:
    
    @allure.title("Valid user can login successfully")
    @allure.description("Test that a valid user can login with correct credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, driver):
        with allure.step("Navigate to login page"):
            login_page = LoginPage(driver)
            login_page.load()
        
        with allure.step("Enter valid credentials and login"):
            login_page.login("standard_user", "secret_sauce")
        
        with allure.step("Verify successful login"):
            assert login_page.is_logged_in(), "User should be logged in successfully"
    
    
    @allure.title("Invalid user cannot login")
    @allure.description("Test that invalid credentials show error message")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, driver):
        with allure.step("Navigate to login page"):
            login_page = LoginPage(driver)
            login_page.load()
        
        with allure.step("Enter invalid credentials"):
            login_page.login("invalid_user", "wrong_password")
        
        with allure.step("Verify error message is displayed"):
            assert login_page.is_error_displayed(), "Error message should be displayed for invalid login"