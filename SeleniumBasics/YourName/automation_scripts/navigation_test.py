"""
Hands-On 4 | Task 2 - WebDriver Navigation and Window Commands
================================================================
Run directly with: python navigation_test.py
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
from setup_test import build_driver, BASE_URL  # noqa: E402


def run():
    driver = build_driver(headless=False)
    try:
        # --- Step 28: navigate to Simple Form Demo, assert URL, go back ---
        driver.get(BASE_URL)
        simple_form_link = driver.find_element(
            "link text", "Simple Form Demo"
        )
        simple_form_link.click()
        assert "simple-form-demo" in driver.current_url
        print("On Simple Form Demo page:", driver.current_url)

        driver.back()
        assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/") or \
            "selenium-playground" in driver.current_url
        print("Navigated back to:", driver.current_url)

        # --- Step 29: open a second tab, list handles, switch, print title ---
        driver.execute_script('window.open("https://www.google.com");')
        handles = driver.window_handles
        print("Open tab handles:", handles)
        assert len(handles) == 2

        driver.switch_to.window(handles[1])
        print("Second tab title:", driver.title)

        # --- Step 30: switch back to the original tab, take a screenshot ---
        driver.switch_to.window(handles[0])
        screenshot_path = os.path.join(
            os.path.dirname(__file__), "playground_screenshot.png"
        )
        driver.save_screenshot(screenshot_path)
        assert os.path.exists(screenshot_path)
        print("Screenshot saved to:", screenshot_path)

        # --- Step 31: window size ---
        size_before = driver.get_window_size()
        print("Window size before:", size_before)
        driver.set_window_size(1280, 800)
        size_after = driver.get_window_size()
        print("Window size after:", size_after)
        # WHY CONSISTENT WINDOW SIZE MATTERS:
        # Responsive pages change their layout (and sometimes which elements
        # even exist, e.g. a hamburger menu replacing a full nav bar) based
        # on viewport width. If tests run with an unpredictable window size
        # (different on CI vs a laptop, different per machine), the same
        # locator can find a different element - or nothing at all - causing
        # flaky failures that have nothing to do with the app itself. Fixing
        # the size makes runs reproducible across environments.

    finally:
        driver.quit()


if __name__ == "__main__":
    run()
