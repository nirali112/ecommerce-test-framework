from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.products_page import ProductsPage
import time

# Create driver using the same method as conftest
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    print("1. Creating ProductsPage instance...")
    products_page = ProductsPage(driver)
    
    print("2. Loading products page (with login)...")
    products_page.load()
    
    print("3. Adding item to cart...")
    products_page.add_item_to_cart("Sauce Labs Backpack")
    
    print("\n4. Checking cart state...")
    
    # Check cart count
    cart_count = products_page.get_cart_count()
    print(f"   Cart count: {cart_count}")
    
    # Check is_item_in_cart
    in_cart = products_page.is_item_in_cart("Sauce Labs Backpack")
    print(f"   is_item_in_cart result: {in_cart}")
    
    # Manual checks
    print("\n5. Manual verification...")
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        print(f"   ✓ Manual badge check: Found badge with text '{badge.text}'")
    except:
        print("   ✗ Manual badge check: No badge found")
        
    try:
        remove_btn = driver.find_element(By.ID, "remove-sauce-labs-backpack")
        print(f"   ✓ Manual remove button check: Found remove button")
    except:
        print("   ✗ Manual remove button check: No remove button found")
    
    print("\n6. Page URL:", driver.current_url)
    
    input("\nPress Enter to close browser...")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to close browser...")
finally:
    driver.quit()