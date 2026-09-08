"""
test_e2e_workflow.py

End-to-end automation of the assignment workflow using the Page Object
Model (POM):

1. Login
2. Hover over PIM and click into it
3. Add 3-4 employees
4. Navigate to Employee List, scroll/paginate, verify each employee's
   name is present, printing "Name Verified" for each
5. Logout

Run with:
    pytest -s tests/test_e2e_workflow.py
"""

import sys
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage
from pages.add_employee_page import AddEmployeePage
from pages.employee_list_page import EmployeeListPage

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"

EMPLOYEES_TO_ADD = [
    ("Ravi", "Kumar"),
    ("Sara", "Ali"),
    ("John", "Smith"),
    ("Meera", "Nair"),
]


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # uncomment to run headless
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


def test_full_workflow(driver):
    # ---- 1. Login ----
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard did not load after login"

    # ---- 2. Hover over PIM and click ----
    dashboard_page.hover_and_click_pim()

    pim_page = PimPage(driver)
    assert "pim" in driver.current_url.lower(), "Did not navigate to PIM module"

    # ---- 3. Add 3-4 employees ----
    added_full_names = []
    for first, last in EMPLOYEES_TO_ADD:
        pim_page.click_add_employee()
        add_employee_page = AddEmployeePage(driver)
        add_employee_page.add_employee(first, last)
        added_full_names.append(f"{first} {last}")

        # Navigate back to the Employee List / Add form for the next employee
        driver.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList"
        )
        time.sleep(1)

    # ---- 4. Verify employees in Employee List ----
    employee_list_page = EmployeeListPage(driver)
    not_found = employee_list_page.verify_employees_present(added_full_names)
    assert not not_found, f"These employees were not found in the list: {not_found}"

    # ---- 5. Logout ----
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    dashboard_page.logout()

    login_page_again = LoginPage(driver)
    assert login_page_again.is_visible(
        login_page_again.USERNAME_INPUT, timeout=10
    ), "Logout did not return user to the login page"
