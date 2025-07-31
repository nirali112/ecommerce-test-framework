import pytest
import allure
from page_objects.products_page import ProductsPage


@allure.feature("Shopping Cart")
@allure.story("Add Products to Cart")
class TestAddToCart:
    
    @allure.title("User can add product to shopping cart")
    @allure.description("Test that a user can successfully add a product to their shopping cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_item_to_cart(self, driver):
        with allure.step("Navigate to products page"):
            products_page = ProductsPage(driver)
            products_page.load()
        
        with allure.step("Add 'Sauce Labs Backpack' to cart"):
            products_page.add_item_to_cart("Sauce Labs Backpack")
        
        with allure.step("Verify item is added to cart"):
            assert products_page.is_item_in_cart("Sauce Labs Backpack"), \
                "Sauce Labs Backpack should be in the cart"
            
            cart_count = products_page.get_cart_count()
            allure.attach(
                str(cart_count),
                name="Cart item count",
                attachment_type=allure.attachment_type.TEXT
            )
            assert cart_count == 1, f"Cart should contain 1 item, but has {cart_count}"