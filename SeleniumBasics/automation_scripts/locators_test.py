"""
Hands-On 5 | Task 1 - Locator Strategies, From Simple to Robust
================================================================
Target: Simple Form Demo message input (id="user-message") and
        Checkbox Demo option labels.

NOTE: If you inspect the live page in DevTools and an attribute below has
changed, update the locator - that's exactly the kind of drift this
exercise is meant to teach you to notice.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from setup_test import build_driver, BASE_URL  # noqa: E402
from selenium.webdriver.common.by import By


def task1_all_locator_strategies():
    driver = build_driver()
    try:
        driver.get(BASE_URL + "simple-form-demo/")

        # 1. By ID - fastest, most stable, preferred when available.
        el_id = driver.find_element(By.ID, "user-message")

        # 2. By NAME - stable if the form uses meaningful name attributes.
        el_name = driver.find_element(By.NAME, "message")

        # 3. By CLASS_NAME - fragile if the class is shared by many elements
        #    or is a styling class rather than a semantic one.
        el_class = driver.find_element(By.CLASS_NAME, "form-control")

        # 4. By TAG_NAME - locates the first matching <input>; too broad to
        #    use alone on a page with multiple inputs, shown here for
        #    completeness only.
        el_tag = driver.find_elements(By.TAG_NAME, "input")[0]

        # 5. By XPATH - absolute path (BAD: brittle, breaks with any DOM change)
        el_xpath_abs = driver.find_element(
            By.XPATH, "/html/body//div[contains(@class,'container')]//input[@id='user-message']"
        )

        # 6. By XPATH - relative path using an attribute (GOOD: resilient)
        el_xpath_rel = driver.find_element(By.XPATH, "//input[@id='user-message']")

        for name, el in [
            ("ID", el_id), ("NAME", el_name), ("CLASS_NAME", el_class),
            ("TAG_NAME", el_tag), ("XPATH absolute", el_xpath_abs),
            ("XPATH relative", el_xpath_rel),
        ]:
            assert el is not None
            print(f"{name}: found element, placeholder='{el.get_attribute('placeholder')}'")

        # Task 33: three CSS selectors for the same element
        css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        css_by_attr = driver.find_element(By.CSS_SELECTOR, "input[name='message']")
        css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
        for name, el in [
            ("CSS by id", css_by_id),
            ("CSS by attribute", css_by_attr),
            ("CSS parent>child", css_by_parent_child),
        ]:
            assert el is not None
            print(f"{name}: OK")

    finally:
        driver.quit()


def task34_checkbox_xpath_text():
    driver = build_driver()
    try:
        driver.get(BASE_URL + "checkbox-demo/")

        # Exact text match
        option_1 = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        print("Exact text() match:", option_1.text)

        # Partial / contains() match - returns every label containing "Option"
        all_options = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print(f"contains() matched {len(all_options)} option labels")
        assert len(all_options) >= 1

    finally:
        driver.quit()


def task35_locator_ranking():
    """
    Step 35: Rank the 6 locator strategies, most to least preferred.

    1. ID              - unique per page (should be), fastest lookup, and
                          reads clearly in code. Best choice whenever present.
    2. CSS_SELECTOR    - almost as fast as ID, very readable, supports
                          attribute/child/sibling matching without XPath's
                          verbosity. Preferred over XPath when it can express
                          the same condition.
    3. NAME            - stable when forms use meaningful `name` attributes
                          (often required for server-side form submission,
                          so it tends not to change casually).
    4. XPATH (relative, attribute-based) - use when CSS cannot express the
                          condition, e.g. matching on visible text, or
                          walking to a parent/ancestor element.
    5. CLASS_NAME      - brittle: styling classes change often and are
                          frequently shared across many unrelated elements.
    6. TAG_NAME / XPATH absolute path - least preferred. Tag name alone is
                          almost never unique; an absolute XPath
                          (/html/body/div[2]/...) breaks the instant any
                          ancestor element is added, removed, or reordered.
    """
    pass


if __name__ == "__main__":
    task1_all_locator_strategies()
    task34_checkbox_xpath_text()
