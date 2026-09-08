"""
pim_page.py
Page Object for the PIM > Employee List landing page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PimPage(BasePage):
    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    EMPLOYEE_LIST_TAB = (By.XPATH, "//a[contains(text(),'Employee List')]")
    EMPLOYEE_NAME_SEARCH = (
        By.XPATH,
        "//label[text()='Employee Name']/../../div[contains(@class,'oxd-autocomplete')]/div/input",
    )
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[contains(.,'Reset')]")
    RESULT_ROWS = (By.XPATH, "//div[@class='oxd-table-card']")

    def click_add_employee(self):
        self.click(self.ADD_EMPLOYEE_BUTTON)

    def open_employee_list(self):
        self.click(self.EMPLOYEE_LIST_TAB)

    def search_employee_by_name(self, name):
        name_field = self.find_clickable(self.EMPLOYEE_NAME_SEARCH)
        name_field.clear()
        name_field.send_keys(name)
        self.wait.until(
            lambda d: len(d.find_elements(By.XPATH, "//div[@role='listbox']//span")) > 0
        )
        self.click((By.XPATH, "//div[@role='listbox']//span"))
        self.click(self.SEARCH_BUTTON)

    def get_result_row_texts(self):
        if self.is_visible(self.RESULT_ROWS, timeout=10):
            return [row.text for row in self.find_all(self.RESULT_ROWS)]
        return []
