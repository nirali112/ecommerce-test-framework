from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create driver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # Login
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Wait for products page
    time.sleep(2)
    
    # Try to add item
    print("Clicking add to cart button...")
    # Try to add item with wait and scroll
    print("Waiting for Add to Cart button...")
    wait = WebDriverWait(driver, 10)
    add_to_cart_button = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )

    # Scroll into view before clicking
    driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
    time.sleep(0.5)  # slight pause for smooth scroll

    print("Clicking add to cart button...")
    add_to_cart_button.click()

    # Wait for either the badge OR the remove button
    time.sleep(2)
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        print(f"✅ Cart badge found! Count: {badge.text}")
    except:
        print("❌ No cart badge found!")
        try:
            remove_button = driver.find_element(By.ID, "remove-sauce-labs-backpack")
            print("✅ Remove button found - item added to cart but badge missing")
        except:
            print("❌ No remove button found either - click might have failed")
        
        input("Press Enter to close...")
    
finally:
    driver.quit()
