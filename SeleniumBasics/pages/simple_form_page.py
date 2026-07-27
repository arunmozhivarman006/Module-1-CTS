"""Hands-On 7 | Task 1 - SimpleFormPage."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    # Locators are class-level constants - if the id ever changes, this is
    # the ONE line that needs updating, not every test that touches it.
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text: str):
        field = self.wait_for_element(self.MESSAGE_INPUT)
        field.clear()
        field.send_keys(text)
        return self

    def click_submit(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()
        return self

    def get_displayed_message(self) -> str:
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
