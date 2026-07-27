"""Hands-On 7 | Task 2 - InputFormPage (Input Form Submit demo)."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):
    NAME_FIELD = (By.NAME, "name")
    EMAIL_FIELD = (By.ID, "inputEmail4")
    PHONE_FIELD = (By.NAME, "phone")
    ADDRESS_FIELD = (By.NAME, "address")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    # The success banner is a text block that appears in place of the form
    # once submission succeeds.
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'Thanks for contacting us')]")
    VALIDATION_ERROR = (By.XPATH, "//*[contains(text(), 'Please fill')]")

    def fill_form(self, name: str, email: str, phone: str, address: str):
        self.wait_for_element(self.NAME_FIELD).send_keys(name)
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone)
        self.driver.find_element(*self.ADDRESS_FIELD).send_keys(address)
        return self

    def submit_form(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()
        return self

    def get_success_message(self) -> str:
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
