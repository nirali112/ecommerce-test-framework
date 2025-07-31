import pytest
import allure
from page_objects.checkout_page import CheckoutPage


@allure.feature("Checkout")
@allure.story("Complete Purchase Flow")
class TestCheckout:
    
    @allure.title("User can complete checkout process")
    @allure.description("Test the complete checkout flow from adding item to order confirmation")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_checkout_flow(self, driver):
        with allure.step("Initialize checkout page and add item to cart"):
            checkout_page = CheckoutPage(driver)
            checkout_page.load()
        
        with allure.step("Complete checkout with customer information"):
            customer_info = {
                "first_name": "John",
                "last_name": "Doe",
                "zip_code": "12345"
            }
            allure.attach(
                str(customer_info),
                name="Customer Information",
                attachment_type=allure.attachment_type.JSON
            )
            checkout_page.perform_checkout(
                customer_info["first_name"],
                customer_info["last_name"],
                customer_info["zip_code"]
            )
        
        with allure.step("Verify order is successful"):
            assert checkout_page.is_order_successful(), \
                "Order should be completed successfully"
            
            success_message = checkout_page.get_success_message()
            allure.attach(
                success_message,
                name="Success Message",
                attachment_type=allure.attachment_type.TEXT
            )