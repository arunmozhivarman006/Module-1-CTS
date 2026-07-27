"""
Hands-On 7 - Page Object Model test suite.

Task 55/56/57: every test below drives the page through a Page Object
method (page.enter_message(...), page.click_submit(), ...). There are
ZERO driver.find_element calls in this file - verify with:
    grep -n "find_element" tests/test_pom_suite.py   # should return nothing

Run the full suite with:
    pytest tests/ -v --html=report.html --self-contained-html
"""

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


# --- Task 55 ---
def test_simple_form_submission_pom(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


# --- Task 56: checkbox via POM ---
def test_checkbox_demo_pom(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")

    page.check_option(1)
    assert page.is_option_checked(1) is True

    page.uncheck_option(1)
    assert page.is_option_checked(1) is False


# --- Task 56: dropdown via POM ---
def test_dropdown_selection_pom(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo/")
    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


# --- Task 57: new Input Form Submit test via InputFormPage ---
def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-submit/")
    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="221B Baker Street",
    )
    page.submit_form()

    assert "thanks for contacting us" in page.get_success_message().lower()


# --- Task 59: maintenance comment ---
"""
If the Submit button's id changed from 'submit' to 'btn-submit' in a flat
(non-POM) script, every test file that clicks that button would need to be
found and edited individually - and it's easy to miss one, leaving a
silently broken test sitting in the suite until it randomly fails in CI.

With POM, the id is declared exactly once as a class-level locator
constant on the relevant page object (e.g. SimpleFormPage.SUBMIT_BUTTON or
InputFormPage.SUBMIT_BUTTON). Fixing the break means editing that single
tuple in that single file; every test that calls page.click_submit() /
page.submit_form() picks up the fix automatically, with no changes needed
in any test file at all.
"""
