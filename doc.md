# 🧪 Swag Labs Automated UI Test Suite  
**File:** `test_saucedemo.py`  
**Author:** Nfomi kingsly nofu 
**Date:** 7/10/2025 
**Framework:** `pytest` + `Selenium WebDriver`

---

## 🏁 Overview
This automated test suite validates the core functionalities of the **Swag Labs** web application  
(https://www.saucedemo.com/) using Selenium WebDriver and `pytest`.

The tests are designed to run on **Google Chrome**, with `ChromeDriverManager` handling driver management automatically.  
It verifies that essential UI and functional flows — such as login, navigation, and error handling — behave correctly.  

Each test captures screenshots for **traceability** and **visual audit**.

---

## 🎯 Purpose
This suite demonstrates **browser-based automated testing** for a live web application.

It supports:
- **Regression testing** (confirming that existing features still work)
- **Functional testing** (verifying user workflows)
- **UI validation** (confirming visual and structural elements)

---

## ⚙️ Key Features

| Feature | Description |
|----------|--------------|
| **Automated Chrome Setup** | Uses `webdriver_manager` to automatically download and manage ChromeDriver. |
| **Fixture-Based Initialization** | Pytest fixture sets up and tears down Chrome sessions automatically. |
| **Temporary Profile Handling** | Each test runs in an isolated Chrome profile for stability. |
| **Screenshot Capture** | Every test takes screenshots, timestamped for audit purposes. |
| **Robust Error Handling** | Validates login, navigation, and page responses with assertions and waits. |

---

## 🧩 Test Architecture

### **1. WebDriver Fixture (`driver`)**
The `driver()` fixture configures and launches Chrome with flags that:
- Disable password manager and pop-up dialogs.
- Prevent autofill and “save password” prompts.
- Use a temporary profile created at runtime and automatically deleted afterward.
- Enable incognito mode to isolate sessions.

**Setup flow:**
1. Create a temporary Chrome profile directory.  
2. Pre-configure Chrome preferences (`Preferences.json`) with password manager disabled.  
3. Launch Chrome through Selenium with these configurations.  
4. Yield the driver to each test, then quit and clean up afterward.

---

## 🧪 Test Cases

### **1️⃣ test_Swag_lab_title**
**Purpose:** Verify that the homepage title is correct.  
**Steps:**
1. Navigate to `https://www.saucedemo.com/`.  
2. Check that the title contains **“Swag Labs.”**  
3. Take a screenshot for validation.  
**Expected Result:** Page title includes *Swag Labs.*

---

### **2️⃣ test_login_without_credentials**
**Purpose:** Verify that the login form enforces required fields.  
**Steps:**
1. Open the login page.  
2. Click **Login** without entering username/password.  
3. Verify that an error message appears.  
4. Take a screenshot of the error.  
**Expected Result:** Error text — *“Epic sadface: Username is required.”*

---

### **3️⃣ test_login_with_wrong_credentials**
**Purpose:** Validate system handling of incorrect login data.  
**Steps:**
1. Open the login page.  
2. Enter invalid username and password.  
3. Click **Login**.  
4. Verify that the correct error appears.  
5. Take a screenshot of the error message.  
**Expected Result:** Error text — *“Epic sadface: Username and password do not match any user in this service.”*

---

### **4️⃣ test_login_with_valid_credentials**
**Purpose:** Verify successful login using valid credentials.  
**Steps:**
1. Navigate to the login page.  
2. Enter:
   - Username: `standard_user`
   - Password: `secret_sauce`  
3. Click **Login.**  
4. Verify navigation to inventory page (`inventory.html`).  
5. Confirm “Products” title is visible.  
6. Capture screenshot of the logged-in page.  
**Expected Result:** Login succeeds and user is redirected to *inventory.html.*

---

### **5️⃣ test_navigate_to_about_after_login**
**Purpose:** Confirm navigation from the inventory page to the **About** section.  
**Steps:**
1. Log in with valid credentials.  
2. Click the hamburger menu (☰).  
3. Select **About** from the menu.  
4. Wait for redirection to the Sauce Labs website.  
5. Take a screenshot of the About page.  
**Expected Result:** Redirects successfully to a page containing *“saucelabs.com.”*

---

## 🧠 Environment Setup

### **Software Requirements**
- Python 3.x  
- pytest  
- selenium  
- webdriver_manager  
- Google Chrome (latest stable version)

### **Hardware Requirements**
- Any modern computer (Windows/macOS/Linux)
- Minimum 2 GB RAM (recommended)

---

## 🧰 Running the Tests

### Run All Tests
```bash
pytest test_saucedemo.py -v
