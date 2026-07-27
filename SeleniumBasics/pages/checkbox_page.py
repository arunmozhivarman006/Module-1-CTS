"""Hands-On 7 | Task 1 - CheckboxPage."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    # The "List of Checkboxes" block on the Checkbox Demo page renders each
    # option as a numbered checkbox input inside a <li>. We locate them by
    # 1-based position among the list checkboxes.
    OPTION_CHECKBOX = "//div[@id='checkbox-demo']//ul//input[@type='checkbox']"

    def _checkbox(self, index: int):
        checkboxes = self.driver.find_elements(By.XPATH, self.OPTION_CHECKBOX)
        return checkboxes[index - 1]

    def check_option(self, index: int):
        box = self._checkbox(index)
        if not box.is_selected():
            box.click()
        return self

    def uncheck_option(self, index: int):
        box = self._checkbox(index)
        if box.is_selected():
            box.click()
        return self

    def is_option_checked(self, index: int) -> bool:
        return self._checkbox(index).is_selected()
