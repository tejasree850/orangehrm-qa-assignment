"""
add_employee_page.py
Page Object for the PIM > Add Employee form.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AddEmployeePage(BasePage):
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    SAVE_BUTTON = (By.XPATH, "//button[contains(.,'Save')]")
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")

    def add_employee(self, first_name, last_name):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)
        # Wait for the app to redirect back to the employee's personal details
        # page, which confirms the save succeeded.
        self.wait.until(lambda d: "viewPersonalDetails" in d.current_url)
