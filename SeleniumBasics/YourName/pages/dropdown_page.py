"""Hands-On 7 | Task 1 - DropdownPage."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class DropdownPage(BasePage):
    DAY_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name: str):
        dropdown_el = self.wait_for_element(self.DAY_DROPDOWN)
        Select(dropdown_el).select_by_visible_text(day_name)
        return self

    def get_selected_day(self) -> str:
        dropdown_el = self.wait_for_element(self.DAY_DROPDOWN)
        return Select(dropdown_el).first_selected_option.text
