from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def load(self):
        """Navigate to the products page (requires login first)"""
        self.driver.get("https://www.saucedemo.com/")
        # Login with standard user
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.username_field)).send_keys("standard_user")
        self.driver.find_element(*self.password_field).send_keys("secret_sauce")
        self.driver.find_element(*self.login_button).click()
        # Wait for products page to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_container")))

    def add_item_to_cart(self, item_name):
        """Add a specific item to cart by its name"""
        wait = WebDriverWait(self.driver, 10)
        
        # Map item names to their add-to-cart button IDs
        item_button_map = {
            "Sauce Labs Backpack": "add-to-cart-sauce-labs-backpack",
            "Sauce Labs Bike Light": "add-to-cart-sauce-labs-bike-light",
            "Sauce Labs Bolt T-Shirt": "add-to-cart-sauce-labs-bolt-t-shirt",
            "Sauce Labs Fleece Jacket": "add-to-cart-sauce-labs-fleece-jacket",
            "Sauce Labs Onesie": "add-to-cart-sauce-labs-onesie",
            "Test.allTheThings() T-Shirt (Red)": "add-to-cart-test.allthethings()-t-shirt-(red)"
        }
        
        if item_name in item_button_map:
            button_id = item_button_map[item_name]
            add_button = (By.ID, button_id)
            wait.until(EC.element_to_be_clickable(add_button)).click()
        else:
            raise ValueError(f"Unknown item: {item_name}")

    def get_cart_count(self):
        """Get the number of items in cart"""
        try:
            wait = WebDriverWait(self.driver, 5)
            badge = wait.until(EC.presence_of_element_located(self.cart_badge))
            return int(badge.text)
        except:
            return 0
    
    def is_item_in_cart(self, item_name = None):
        """Check if item was added to cart (cart count > 0)"""
        return self.get_cart_count() > 0