"""
Hands-On 6 - pytest test suite for the Selenium Playground.

These tests use the driver directly (no Page Objects yet - that refactor
happens in Hands-On 7 / test_pom_suite.py). Run with:
    pytest tests/test_playground.py -v --html=report.html --self-contained-html
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# --- Task 42 ---
def test_simple_form_submission(driver, base_url):
    driver.get(base_url + "simple-form-demo/")
    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys("Hello Selenium")
    driver.find_element(By.ID, "showInput").click()

    displayed = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed.text == "Hello Selenium"


# --- Task 43 ---
def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")
    first_checkbox = driver.find_element(
        By.XPATH, "(//div[@id='checkbox-demo']//ul//input[@type='checkbox'])[1]"
    )

    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False


# --- Task 45: parameterised form submission ---
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission_parametrized(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")
    driver.find_element(By.ID, "user-message").send_keys(message)
    driver.find_element(By.ID, "showInput").click()

    displayed = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed.text == message


# --- Task 49 ---
def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo/")
    dropdown_el = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_el)

    select.select_by_visible_text("Wednesday")

    assert select.first_selected_option.text == "Wednesday"
