"""
login_page.py
Page Object for the OrangeHRM Login screen.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_ALERT = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    REQUIRED_FIELD_MSGS = (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]")

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        if self.is_visible(self.ERROR_ALERT, timeout=10):
            return self.find(self.ERROR_ALERT).text
        return None

    def get_required_field_messages(self):
        if self.is_visible(self.REQUIRED_FIELD_MSGS, timeout=5):
            return [el.text for el in self.find_all(self.REQUIRED_FIELD_MSGS)]
        return []
