"""
test_Swag_Lab.py

Automated UI tests for the Swag Labs website using Selenium WebDriver and pytest.

This test suite verifies basic page functionality and content, including:
- Page title verification
- Login verification
- Page navigation and interaction with elements such as links
- Saves screenshot of every test stage for audit and traceability purposes.

Requirements:
- Python 3.x
- Selenium
- pytest
- webdriver_manager

The tests are designed to be run with Chrome, using ChromeDriverManager to manage the driver.
Some `time.sleep()` calls are used for demo purposes to allow visual confirmation during test runs.
"""

from xml.dom.xmlbuilder import Options
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile, shutil, os
import json



@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # 1) Hard-disable PW manager & leak detection via flags/prefs
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-features=PasswordManagerOnboarding,PasswordLeakDetection,AutofillKeychain,AutofillServerCommunication")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "credentials_enable_autosignin": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
        "safebrowsing.enabled": False  # test only
    })
    # reduce Chrome automation noise
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 2) Create a fresh profile and pre-write the Preferences file
    temp_profile = tempfile.mkdtemp(prefix="chrome-prof-")
    default_dir = os.path.join(temp_profile, "Default")
    os.makedirs(default_dir, exist_ok=True)

    # Preseed Preferences so Chrome starts with these disabled
    prefs_path = os.path.join(default_dir, "Preferences")
    prefs_json = {
        "credentials_enable_service": False,
        "profile": {
            "password_manager_enabled": False
        },
        "autofill": {
            "enabled": False
        },
        "safebrowsing": {
            "enabled": False
        },
        # This can help prevent Google account interstitials in some envs
        "signin": {
            "allowed": False
        }
    }
    with open(prefs_path, "w", encoding="utf-8") as f:
        json.dump(prefs_json, f)

    options.add_argument(f"--user-data-dir={temp_profile}")
    options.add_argument("--profile-directory=Default")

    # 3) Extra isolation that often kills the bubble entirely
    options.add_argument("--incognito")   # PW manager is off in incognito
    # OR: options.add_argument("--guest") # even stricter, try this if needed

    # your original zoom arg
    options.add_argument("--force-device-scale-factor=0.5")

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    try:
        yield driver
    finally:
        driver.quit()
        shutil.rmtree(temp_profile, ignore_errors=True)


# @pytest.mark.skip(reason="Skipping this test for demo")  # comment to enable the test
def test_Swag_lab_title(driver):
    """
    Verify that the Swag Labs homepage has the correct page title.

    Steps:
    1. Open the Swag Labs homepage.
    2. Optionally wait to visually confirm the page load.
    3. Assert that the page title matches the expected string.
    4. Take a screenshot of the page.

    Args:
        driver (webdriver.Chrome): Selenium WebDriver fixture.
    """
    print("Checking for correct page title")
    
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)  # not required, but pause so you can see the page
    
    assert "Swag Labs" in driver.title # use the Selenium's built-in property
        
    timestamp = int(time.time())
    screenshot_file = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_file) # take a screenshot to verify how the home page looked like
    print(f"Screenshot saved to {screenshot_file}")

    time.sleep(2)  # not required, but pause so you can see the page



# @pytest.mark.skip(reason="Skipping this test for demo")  # comment to enable the test
def test_login_without_credentials(driver):
    """
    Test that clicking login without entering username/password shows an error.
    
    Steps:
    1. Open the Swag Labs homepage
    2. Click the login button without entering credentials
    3. Verify error message appears with correct text
    4. Take a screenshot of the error message
    
    Args:
        driver (webdriver.Chrome): Selenium WebDriver fixture.
    """
    print("Testing login without credentials")
    
    # Navigate to the page
    driver.get("https://www.saucedemo.com/")
    
    # Wait for login button to be clickable and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )
    login_button.click()
    
    # Wait for error message to appear
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    
    # Verify the error message text
    expected_error = "Epic sadface: Username is required"
    assert expected_error in error_message.text, \
        f"Expected error: '{expected_error}', but got: '{error_message.text}'"
    
    print(f"✓ Error message displayed correctly: {error_message.text}")

    timestamp = int(time.time())
    screenshot_file = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_file) # take a screenshot to verify the error message with no credentials
    print(f"Screenshot saved to {screenshot_file}")
    
    time.sleep(2)  # Optional: pause to visually verify


# @pytest.mark.skip(reason="Skipping this test for demo")  # comment to enable the test
def test_login_with_wrong_credentials(driver):
    """
    Test that logging in with incorrect username and password shows an error.
    
    Steps:
    1. Open the Swag Labs homepage
    2. Enter invalid username and password
    3. Click the login button
    4. Verify error message appears with correct text
    5. Take a screenshot of the error message
    
    Args:
        driver (webdriver.Chrome): Selenium WebDriver fixture.
    """
    print("Testing login with wrong credentials")
    
    # Navigate to the page
    driver.get("https://www.saucedemo.com/")
    
    # Enter invalid username
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("kingsley")
    
    # Enter invalid password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("djdskjsfhfak")
    
    # Click login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    
    # Wait for error message to appear
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    
    # Verify the error message text
    expected_error = "Epic sadface: Username and password do not match any user in this service"
    assert expected_error in error_message.text, \
        f"Expected error: '{expected_error}', but got: '{error_message.text}'"
    
    print(f"✓ Error message displayed correctly: {error_message.text}")
    
    timestamp = int(time.time())
    screenshot_file = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_file) # take a screenshot to verify the error message with wrong credentials
    print(f"Screenshot saved to {screenshot_file}")

    time.sleep(5)  # Optional: pause to visually verify



# @pytest.mark.skip(reason="Skipping this test for demo")  # comment to enable the test
def test_login_with_valid_credentials(driver):
    """
    Test successful login with valid username and password.
    
    Steps:
    1. Open the Swag Labs homepage
    2. Enter valid username and password
    3. Click the login button
    4. Verify successful login by checking the inventory page URL and title
    5. Take a screenshot of the inventory page
    
    Args:
        driver (webdriver.Chrome): Selenium WebDriver fixture.
    """
    print("Testing login with valid credentials")
    
    # Navigate to the page
    driver.get("https://www.saucedemo.com/")
    
    # Enter valid username
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    
    # Enter valid password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    
    # Click login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    
    # Wait for the inventory page to load
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )
    
    # Verify we're on the inventory page
    assert "inventory.html" in driver.current_url, \
        f"Expected URL to contain 'inventory.html', but got: {driver.current_url}"
    
    # Verify the page title
    assert "Swag Labs" in driver.title
    
    # Verify the products page header is visible
    page_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
    assert page_title.text == "Products", \
        f"Expected page title 'Products', but got: '{page_title.text}'"
    
    print(f"✓ Successfully logged in! Current URL: {driver.current_url}")
    print(f"✓ Page title: {page_title.text}")
    
    timestamp = int(time.time())
    screenshot_file = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_file) # take a screenshot to confirm the login was successful
    print(f"Screenshot saved to {screenshot_file}")

    time.sleep(2)  # Optional: pause to visually verify


# @pytest.mark.skip(reason="Skipping this test for demo")  # comment to enable the test
def test_navigate_to_about_after_login(driver):
    """
    Test navigation to About page after successful login.
    
    Steps:
    1. Login with valid credentials
    2. Wait for inventory page to load
    3. Click hamburger menu (3 horizontal lines in top-left)
    4. Click "About" from the menu
    5. Verify navigation to Sauce Labs About page
    6. Take a screenshot of the About page
    
    Args:
        driver (webdriver.Chrome): Selenium WebDriver fixture.
    """
    print("\n=== Testing Navigation to About Page ===")
    
    # Step 1: Navigate to login page
    driver.get("https://www.saucedemo.com/")
    print("✓ Opened Swag Labs login page")
    
    # Step 2: Enter credentials and login
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    username_field.send_keys("standard_user")
    print("✓ Entered username")
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    print("✓ Entered password")
    
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    print("✓ Clicked login button")
    
    # Step 3: Wait for successful login (inventory page loads)
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )
    print("✓ Successfully logged in - on inventory page")
    
    # Wait a moment for page to fully load
    time.sleep(1)
    
    # Step 4: Click the hamburger menu (3 lines in top-left corner)
    hamburger_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    hamburger_menu.click()
    print("✓ Clicked hamburger menu (☰)")
    
    # Wait for menu animation to complete
    time.sleep(1)
    
    # Step 5: Click "About" link from the menu
    about_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "about_sidebar_link"))
    )
    about_link.click()
    print("✓ Clicked 'About' link")
    
    # Step 6: Wait for navigation to Sauce Labs website
    WebDriverWait(driver, 10).until(
        EC.url_contains("saucelabs.com")
    )
    
    # Step 7: Verify we're on the About page
    current_url = driver.current_url
    assert "saucelabs.com" in current_url, \
        f"Expected URL to contain 'saucelabs.com', but got: {current_url}"
    
    print(f"✓ Successfully navigated to About page!")
    print(f"  Current URL: {current_url}")
    
    # Pause to see the result
    time.sleep(3)
    timestamp = int(time.time())
    screenshot_file = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_file) # take a screenshot to verify how the about page looked like
    print(f"Screenshot saved to {screenshot_file}")
    
    time.sleep(2)
    
    print("=== Test Completed Successfully ===\n")

