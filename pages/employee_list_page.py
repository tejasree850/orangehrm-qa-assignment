"""
employee_list_page.py
Page Object for the PIM > Employee List page: scrolling through
pagination/rows and verifying employee names are present.
"""

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class EmployeeListPage(BasePage):
    TABLE_ROWS = (By.XPATH, "//div[@class='oxd-table-body']/div")
    EMPLOYEE_NAME_CELL = (By.XPATH, ".//div[@class='oxd-table-cell'][3]")
    NEXT_PAGE_BUTTON = (By.XPATH, "//li[contains(@class,'next')]/button")
    RECORDS_FOUND_TEXT = (By.XPATH, "//span[contains(@class,'oxd-text--span')]")

    def get_all_visible_names(self):
        """Collect employee full names from every row currently rendered."""
        names = []
        rows = self.find_all(self.TABLE_ROWS)
        for row in rows:
            try:
                cell = row.find_element(*self.EMPLOYEE_NAME_CELL)
                names.append(cell.text.strip())
            except Exception:
                continue
        return names

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(1)

    def verify_employees_present(self, expected_names):
        """
        Scrolls through the employee list (and paginates if needed) looking
        for every name in expected_names. Prints 'Name Verified' for each
        one found, and returns the list of names that were NOT found.
        """
        expected_remaining = set(expected_names)
        found = set()

        max_pages = 20  # safety limit to avoid an infinite loop
        for _ in range(max_pages):
            self.scroll_to_bottom()
            visible_names = self.get_all_visible_names()

            for name in list(expected_remaining):
                if any(name in visible_name for visible_name in visible_names):
                    print(f"{name}: Name Verified")
                    found.add(name)
                    expected_remaining.discard(name)

            if not expected_remaining:
                break

            next_buttons = self.driver.find_elements(*self.NEXT_PAGE_BUTTON)
            if next_buttons and next_buttons[0].is_enabled():
                next_buttons[0].click()
                time.sleep(1.5)
            else:
                break

        not_found = list(expected_remaining)
        if not_found:
            print(f"Could not verify: {not_found}")
        return not_found
