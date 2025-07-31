from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    @allure.step("Load products page")
    def load(self):
        """Navigate to the products page (requires login first)"""
        with allure.step("Navigate to SauceDemo website"):
            self.driver.get("https://www.saucedemo.com/")
            
        with allure.step("Login as standard user"):
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(self.username_field)).send_keys("standard_user")
            self.driver.find_element(*self.password_field).send_keys("secret_sauce")
            self.driver.find_element(*self.login_button).click()
            
        with allure.step("Wait for products page to load"):
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_container")))
            # Add extra wait to ensure page is fully loaded
            time.sleep(2)  # Increased wait time
            allure.attach(
                self.driver.current_url,
                name="Products Page URL",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.step("Add item '{item_name}' to cart")
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
            
            with allure.step(f"Click 'Add to cart' button for {item_name}"):
                print(f"DEBUG: Looking for button with ID: {button_id}")
                
                # Wait for button to be clickable
                button_element = wait.until(EC.element_to_be_clickable(add_button))
                print(f"DEBUG: Button found, text: '{button_element.text}'")
                
                # Scroll into view before clicking
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
                time.sleep(0.5)  # slight pause for smooth scroll
                
                # Try multiple click methods
                try:
                    print("DEBUG: Trying regular click...")
                    button_element.click()
                except Exception as e:
                    print(f"DEBUG: Regular click failed: {e}")
                    print("DEBUG: Trying JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", button_element)
                
                # Wait for cart to update
                print("DEBUG: Waiting 2 seconds for cart update...")
                time.sleep(2)
                
                # Check what happened
                try:
                    badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
                    print(f"DEBUG: Badge found after click! Text: {badge.text}")
                except:
                    print("DEBUG: No badge found after click")
                    
                try:
                    remove_btn = self.driver.find_element(By.ID, f"remove-{button_id.replace('add-to-cart-', '')}")
                    print("DEBUG: Remove button found - item was added!")
                except:
                    print("DEBUG: No remove button found")
                
                # Take screenshot after clicking
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name=f"After adding {item_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        else:
            raise ValueError(f"Unknown item: {item_name}")

    @allure.step("Get cart item count")
    def get_cart_count(self):
        """Get the number of items in cart"""
        try:
            # Don't wait too long - badge should be there already
            badge = self.driver.find_element(*self.cart_badge)
            count = int(badge.text)
            
            print(f"DEBUG: get_cart_count found badge with count: {count}")
            
            allure.attach(
                str(count),
                name="Current cart count",
                attachment_type=allure.attachment_type.TEXT
            )
            return count
        except Exception as e:
            print(f"DEBUG: get_cart_count error: {e}")
            allure.attach(
                f"No cart badge found: {str(e)}",
                name="Cart badge error",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Cart state when badge not found",
                attachment_type=allure.attachment_type.PNG
            )
            return 0
    
    @allure.step("Check if item is in cart")
    def is_item_in_cart(self, item_name=None):
        """Check if item was added to cart"""
        print(f"DEBUG: is_item_in_cart called with item_name={item_name}")
        
        # First try to check cart count
        cart_count = self.get_cart_count()
        if cart_count > 0:
            print(f"DEBUG: Cart count > 0, returning True")
            return True
        
        # If no cart badge, check if remove button exists (alternative confirmation)
        if item_name:
            item_button_map = {
                "Sauce Labs Backpack": "remove-sauce-labs-backpack",
                "Sauce Labs Bike Light": "remove-sauce-labs-bike-light",
                "Sauce Labs Bolt T-Shirt": "remove-sauce-labs-bolt-t-shirt",
                "Sauce Labs Fleece Jacket": "remove-sauce-labs-fleece-jacket",
                "Sauce Labs Onesie": "remove-sauce-labs-onesie",
                "Test.allTheThings() T-Shirt (Red)": "remove-test.allthethings()-t-shirt-(red)"
            }
            
            if item_name in item_button_map:
                remove_button_id = item_button_map[item_name]
                print(f"DEBUG: Checking for remove button: {remove_button_id}")
                try:
                    self.driver.find_element(By.ID, remove_button_id)
                    print("DEBUG: Remove button found!")
                    allure.attach(
                        f"Remove button found for {item_name}",
                        name="Item confirmed in cart",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    return True
                except:
                    print("DEBUG: Remove button not found")
                    pass
        
        print("DEBUG: Returning False - no cart badge or remove button")
        return False