"""Hands-On 7 | Task 1 - BasePage: shared behaviour for every page object."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Common functionality every page object inherits.

    Golden rule of POM: page objects contain INTERACTIONS (how to do
    something) and return VALUES. They never contain `assert` statements -
    assertions belong in the test files, which decide what "correct" means.
    """

    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url: str):
        self.driver.get(url)
        return self

    def get_title(self) -> str:
        return self.driver.title

    def wait_for_element(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
