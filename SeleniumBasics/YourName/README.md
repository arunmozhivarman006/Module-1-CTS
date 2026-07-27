# Selenium Basics — Hands-On 4 to 7 (Digital Nurture 5.0)

Completed: Hands-On 4 (WebDriver setup & navigation), Hands-On 5 (locators & waits),
Hands-On 6 (pytest integration), Hands-On 7 (Page Object Model).

> **Heads up:** LambdaTest has rebranded to **TestMu AI**. The old
> `lambdatest.com/selenium-playground` URLs used throughout this exercise
> book still work (they redirect), so all scripts here use the original
> URLs from the exercise book. If a locator ever stops matching, open
> DevTools (F12) on the live page and update the relevant `By.ID` /
> `By.XPATH` value — that's a normal part of maintaining a Selenium suite.

## Folder structure

```
SeleniumBasics/<YourName>/
├── requirements.txt
├── pytest.ini
├── README.md
├── automation_scripts/       # Hands-On 4 & 5 — standalone scripts
│   ├── setup_test.py         # HO4 Task 1 — architecture notes + driver setup
│   ├── navigation_test.py    # HO4 Task 2 — navigation, tabs, screenshots
│   ├── locators_test.py      # HO5 Task 1 — all 6 locator strategies
│   └── waits_test.py         # HO5 Task 2 — WebDriverWait / ExpectedConditions
├── pages/                    # Hands-On 7 — Page Object classes
│   ├── base_page.py
│   ├── simple_form_page.py
│   ├── checkbox_page.py
│   ├── dropdown_page.py
│   └── input_form_page.py
└── tests/                    # Hands-On 6 & 7 — pytest suite
    ├── conftest.py           # driver + base_url fixtures, failure screenshots
    ├── test_playground.py    # HO6 — flat pytest tests, parametrized
    └── test_pom_suite.py     # HO7 — same scenarios refactored onto POM
```

## Setup

```
pip install -r requirements.txt
```

## Running things

Standalone scripts (Hands-On 4 & 5):
```
python automation_scripts/setup_test.py
python automation_scripts/navigation_test.py
python automation_scripts/locators_test.py
python automation_scripts/waits_test.py
```

Full pytest suite (Hands-On 6 & 7), from the project root:
```
pytest tests/ -v --html=report.html --self-contained-html
```

## Pushing this to GitHub without using the command line

You don't need `git` on the command line at all — **GitHub Desktop** does
everything through buttons/menus.

1. **Install GitHub Desktop**: https://desktop.github.com/ and sign in with
   your GitHub account.
2. In GitHub Desktop: **File → New Repository**.
   - Name: `SeleniumBasics` (or whatever your submission naming convention is)
   - Local path: pick the folder that will contain this `<YourName>/` folder
   - Leave "Initialize with a README" unchecked if you already have one.
3. Copy this entire `SeleniumBasics/<YourName>/` folder into that new local
   repository folder (drag-and-drop in Finder/Explorer works fine).
4. Back in GitHub Desktop, you'll see all the new files listed under
   **Changes** on the left. Add a summary (e.g. "Add Hands-On 4-7
   Selenium solutions") in the box at the bottom-left, then click
   **Commit to main**.
5. Click **Publish repository** in the top bar (first time), or **Push
   origin** (subsequent commits). Choose public/private as required by
   your program, then confirm.
6. Your repo URL will be `https://github.com/<your-username>/<repo-name>`
   — that's the link to share with your POC.

**Alternative with zero installs**, if you'd rather not install anything:
1. Go to https://github.com/new and create the empty repository in your
   browser.
2. Open the repository page → **Add file → Upload files**.
3. Drag the whole `SeleniumBasics/<YourName>/` folder (or its contents) into
   the upload area, add a commit message at the bottom, and click
   **Commit changes**.
   - Note: browser upload preserves subfolders when you drag a folder in
     modern Chrome/Edge/Firefox, but if it flattens them, upload one
     subfolder (`automation_scripts/`, `pages/`, `tests/`) at a time using
     **Add file → Upload files** repeatedly, into the matching folder path.

Either way, no terminal or `git` commands are required.
