"""
Hands-On 6 - Shared pytest fixtures for the Selenium Playground suite.
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "failure_screenshots")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Task 48: session-scoped constant reused by every test instead of
    hardcoding the URL in each test function."""
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    """
    Task 41: function-scoped fixture -> a brand-new Chrome instance per test.
    scope='function' (the default) means every test gets an isolated
    browser, so one test's leftover state (cookies, open tabs, filled
    fields) can never leak into the next test. scope='session' would reuse
    a single browser across the whole run - faster, but tests can then
    interfere with each other, which makes failures harder to diagnose.
    """
    options = Options()
    # Uncomment for headless CI runs:
    # options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    drv.set_window_size(1280, 800)

    yield drv  # --- setup above, teardown below ---

    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Task 46: capture a screenshot automatically whenever a test fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            safe_name = item.name.replace("/", "_").replace("::", "_")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}_failure.png")
            try:
                driver_fixture.save_screenshot(screenshot_path)
                print(f"\nSaved failure screenshot to {screenshot_path}")
            except Exception as exc:  # pragma: no cover - best-effort capture
                print(f"\nCould not capture failure screenshot: {exc}")
