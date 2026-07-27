"""
Hands-On 5 | Task 2 - WebDriverWait and Expected Conditions
================================================================
Target: Bootstrap Alerts demo (bootstrap-alert-messages-demo).
"""

import os
import sys
import time

sys.path.append(os.path.dirname(__file__))
from setup_test import build_driver, BASE_URL  # noqa: E402
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

ALERTS_URL = BASE_URL + "bootstrap-alert-messages-demo/"


def task36_explicit_wait_for_alert():
    driver = build_driver()
    try:
        driver.get(ALERTS_URL)
        # The "Success Message" trigger button - located by its visible text
        # rather than a guessed id, since button ids on this demo can vary.
        success_button = driver.find_element(By.XPATH, "//button[contains(., 'Success')]")
        success_button.click()

        alert_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert_box.text.lower()
        print("Success alert text:", alert_box.text)
    finally:
        driver.quit()


def task37_sleep_vs_explicit_wait():
    """Compare a hard sleep against an explicit wait for the same assertion."""
    # --- Version A: time.sleep(3) ---
    driver = build_driver()
    try:
        start = time.time()
        driver.get(ALERTS_URL)
        driver.find_element(By.XPATH, "//button[contains(., 'Success')]").click()
        time.sleep(3)  # BAD: always waits the full 3s, even if alert appears in 200ms
        alert_box = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        assert alert_box.is_displayed()
        sleep_duration = time.time() - start
        print(f"time.sleep(3) version took {sleep_duration:.2f}s")
    finally:
        driver.quit()

    # --- Version B: WebDriverWait ---
    driver = build_driver()
    try:
        start = time.time()
        driver.get(ALERTS_URL)
        driver.find_element(By.XPATH, "//button[contains(., 'Success')]").click()
        alert_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert alert_box.is_displayed()
        wait_duration = time.time() - start
        print(f"WebDriverWait version took {wait_duration:.2f}s")
    finally:
        driver.quit()

    # COMMENT: On a fast machine the alert appears almost instantly, so the
    # explicit-wait version finishes in well under a second, while the
    # sleep(3) version is ALWAYS at least 3 seconds no matter how fast the
    # page responds. On a slow/loaded machine, the opposite risk applies:
    # a fixed sleep(3) might not be long enough and the test fails, while
    # WebDriverWait keeps polling up to its full timeout and still passes.
    # Explicit waits are therefore both faster on average and more reliable.


def task38_element_to_be_clickable():
    driver = build_driver()
    try:
        driver.get(ALERTS_URL)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Success')]"))
        )
        button.click()
        print("Clicked once element_to_be_clickable was satisfied.")
        # DIFFERENCE:
        # visibility_of_element_located only checks that the element is
        # present in the DOM and has a non-zero size (i.e. it is rendered
        # and visible). It says nothing about whether the element can
        # currently be interacted with.
        # element_to_be_clickable performs that same visibility check AND
        # additionally checks that the element is enabled (not disabled)
        # and not obscured by another element on top of it - i.e. that a
        # real click at that point would actually land on the element.
        # A button can be visible but still disabled, or visible but
        # covered by a modal/overlay; only element_to_be_clickable catches
        # both of those cases before attempting the click.
    finally:
        driver.quit()


def task39_fluent_wait_dynamic_table_row():
    """
    FluentWait equivalent in Python: WebDriverWait supports poll_frequency
    and ignored_exceptions directly, giving the same behaviour as Java's
    FluentWait (poll every N ms, ignore certain exceptions, timeout after M s).
    """
    driver = build_driver()
    try:
        driver.get(BASE_URL + "table-sort-search-demo/")

        row = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,  # poll every 500ms
            ignored_exceptions=[NoSuchElementException],
        ).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr")
        )
        print("First dynamically-loaded table row:", row.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    task36_explicit_wait_for_alert()
    task37_sleep_vs_explicit_wait()
    task38_element_to_be_clickable()
    task39_fluent_wait_dynamic_table_row()
