# orangehrm-qa-assignment

# OrangeHRM Automation – QA Assignment 2026

Selenium + Python automation for OrangeHRM demo site, built with the
**Page Object Model (POM)**.

Site under test: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
Credentials: `Admin` / `admin123` (as shown on the login page)

## Project structure

```
orangehrm_automation/
├── pages/
│   ├── base_page.py           # shared wait helpers
│   ├── login_page.py          # login form locators + actions
│   ├── dashboard_page.py      # navbar, PIM hover/click, logout
│   ├── pim_page.py            # Add Employee button, Employee List tab, search
│   ├── add_employee_page.py   # Add Employee form
│   └── employee_list_page.py  # scroll/paginate + name verification
├── tests/
│   ├── test_login_basic.py    # standalone login-only script
│   └── test_e2e_workflow.py   # full assignment workflow (pytest)
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You also need Chrome + a matching Chromedriver on PATH (or use
`webdriver-manager`, already listed in requirements.txt, and swap
`webdriver.Chrome(options=options)` for:

```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
```

## Running

Standalone login script:
```bash
python tests/test_login_basic.py
```

Full workflow (login → PIM → add employees → verify in list → logout):
```bash
pytest -s tests/test_e2e_workflow.py
```

## What the full workflow does

1. Logs in with valid credentials and confirms the Dashboard loads.
2. Hovers over the **PIM** menu item and clicks it.
3. Clicks **Add Employee** and adds 4 employees, returning to the
   Employee List between each add.
4. Opens **Employee List**, scrolls/paginates through the table, and
   for each added employee prints `"<Name>: Name Verified"` once found.
5. Logs out and confirms the app returns to the login page.

## Notes / assumptions

- Locators are based on the current OrangeHRM demo build's DOM
  structure (className/XPath). If OrangeHRM updates their UI, the
  locators in `pages/*.py` may need small adjustments.
- The demo site periodically resets its data, so re-running the suite
  should always find a clean employee list.
- Explicit waits (`WebDriverWait` + `expected_conditions`) are used
  throughout instead of hard sleeps, except for a couple of short
  `time.sleep()` calls after pagination clicks/page navigations to
  allow the Angular-like SPA to re-render.
