"""
test_login_basic.py

Basic standalone Selenium script (not pytest-dependent) to verify login
functionality, as requested in the assignment. Covers:
  - Valid login
  - Invalid password
  - Blank username & password

Run with:
    python tests/test_login_basic.py
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


def test_valid_login(driver):
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    dashboard_page = DashboardPage(driver)
    result = dashboard_page.is_loaded()
    print(f"[Valid Login] PASS" if result else "[Valid Login] FAIL")
    dashboard_page.logout()
    return result


def test_invalid_password(driver):
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USERNAME, "wrongPassword123")
    error = login_page.get_error_message()
    result = error is not None and "invalid" in error.lower()
    print(f"[Invalid Password] {'PASS' if result else 'FAIL'} - message: {error}")
    return result


def test_blank_credentials(driver):
    login_page = LoginPage(driver).open()
    login_page.login("", "")
    messages = login_page.get_required_field_messages()
    result = len(messages) >= 2
    print(f"[Blank Credentials] {'PASS' if result else 'FAIL'} - messages: {messages}")
    return result


if __name__ == "__main__":
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        results = {
            "valid_login": test_valid_login(driver),
            "invalid_password": test_invalid_password(driver),
            "blank_credentials": test_blank_credentials(driver),
        }
        print("\n--- Summary ---")
        for name, passed in results.items():
            print(f"{name}: {'PASS' if passed else 'FAIL'}")
    finally:
        time.sleep(2)
        driver.quit()
