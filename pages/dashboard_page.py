"""
dashboard_page.py
Page Object for the Dashboard / top navigation bar, including the
PIM hover-and-click interaction and logout.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage


class DashboardPage(BasePage):
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    PIM_MENU_ITEM = (By.XPATH, "//a[@class='oxd-main-menu-item' and contains(., 'PIM')]")
    USER_DROPDOWN = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")

    def is_loaded(self):
        return self.is_visible(self.DASHBOARD_HEADER, timeout=15)

    def hover_and_click_pim(self):
        pim_element = self.find(self.PIM_MENU_ITEM)
        ActionChains(self.driver).move_to_element(pim_element).pause(0.5).click(
            pim_element
        ).perform()

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
