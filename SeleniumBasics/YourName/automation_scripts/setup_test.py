"""
Hands-On 4 | Task 1 - Selenium Architecture & Environment Setup
================================================================

SELENIUM ARCHITECTURE - THREE MAIN COMPONENTS
------------------------------------------------
1. WebDriver
   WebDriver is the core automation API. It is a set of language-specific bindings
   (Python, Java, JS, etc.) that talk to a browser-specific "driver" executable
   (e.g. chromedriver.exe) over the W3C WebDriver HTTP protocol. The driver
   executable then translates those HTTP commands into native browser calls.
   Flow: Test script -> Selenium client library -> JSON wire protocol (HTTP) ->
   Browser driver (chromedriver) -> Native browser automation hooks -> Browser.
   Because it talks directly to the browser (no JavaScript injection needed),
   WebDriver can do things a JS-only tool cannot, such as handling native
   alerts, file uploads, and multiple windows.

2. Selenium Grid
   Grid solves the problem of running tests across many browser/OS
   combinations, or many tests in parallel, without every machine needing its
   own physical browser install. A central "hub" receives test requests and
   routes them to registered "nodes" (machines/containers running specific
   browser + OS combos). This cuts total execution time for large regression
   suites and enables true cross-browser coverage (Chrome on Windows, Safari
   on macOS, etc.) from one test codebase.

3. Selenium IDE
   Selenium IDE is a browser extension for record-and-playback test creation.
   You interact with a page normally (click, type) and the IDE records each
   action as a reusable step. It is useful for quickly prototyping a test flow
   or for non-programmers, and it can export the recorded flow as source code
   (Python, Java, JS, etc.) to be dropped into a "real" WebDriver project. It
   is not meant to replace a maintained WebDriver + pytest suite because
   recorded scripts tend to use brittle, absolute locators.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def build_driver(headless: bool = False) -> webdriver.Chrome:
    """Create a Chrome WebDriver instance using webdriver-manager.

    webdriver-manager automatically downloads and caches the ChromeDriver
    binary that matches the locally installed Chrome version, so we never
    have to manually download/replace chromedriver.exe ourselves.
    """
    options = Options()
    if headless:
        # Task 27: run without a visible browser window.
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Task 26: implicit wait applied globally.
    # WHY THIS IS CONSIDERED BAD PRACTICE:
    # driver.implicitly_wait(10) tells WebDriver to silently retry ANY
    # find_element call for up to 10 seconds before raising
    # NoSuchElementException. That sounds convenient, but:
    #   1. It applies to every single locator call in the whole test run,
    #      even ones that should fail fast (e.g. checking an element is
    #      absent) - this makes negative-assertion tests slow.
    #   2. Mixing implicit waits with explicit waits (WebDriverWait) causes
    #      unpredictable, hard-to-debug total wait times, since both timers
    #      can stack.
    #   3. It only waits for an element to *exist* in the DOM, not for it to
    #      be visible, enabled, or stable - it does not solve the actual
    #      problem of "is this element ready to interact with?" the way
    #      explicit waits + ExpectedConditions do (see Hands-On 5).
    driver.implicitly_wait(10)
    return driver


def test_open_playground_and_print_title():
    driver = build_driver(headless=False)
    try:
        driver.get(BASE_URL)
        print("Page title:", driver.title)
        assert "Selenium" in driver.title or "Playground" in driver.title
    finally:
        driver.quit()


def test_open_playground_headless():
    """Task 27: same navigation, but headless - title should still print."""
    driver = build_driver(headless=True)
    try:
        driver.get(BASE_URL)
        print("Headless page title:", driver.title)
        assert driver.title != ""
    finally:
        driver.quit()


if __name__ == "__main__":
    test_open_playground_and_print_title()
    test_open_playground_headless()
