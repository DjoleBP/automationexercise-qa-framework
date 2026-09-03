# AutomationExercise QA Framework

A Playwright (Python) test automation framework for [automationexercise.com](https://automationexercise.com) — built as a QA automation portfolio piece covering UI + API testing, cross-browser and mobile-emulation coverage, and a full CI/CD pipeline.

[![CI](https://github.com/DjoleBP/automationexercise-qa-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/DjoleBP/automationexercise-qa-framework/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-python-45ba4b)
![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC)

**Latest report:** https://djolebp.github.io/automationexercise-qa-framework/
**Latest CI run:** https://github.com/DjoleBP/automationexercise-qa-framework/actions/workflows/ci.yml

## Why this project exists

This is a portfolio project demonstrating the skills listed in a QA Automation Engineer job
description: test case design, a UI automation framework, API testing, cross-browser/mobile
coverage, CI/CD, and an agile/ticket-driven workflow. Every locator, error message, and API
response documented here was verified against the live site, not guessed from its docs — see
["Verified quirks"](docs/test_plan.md#verified-quirks-worth-knowing) in the test plan.

## Tech stack

- **Language:** Python 3.11+
- **UI automation:** [Playwright for Python](https://playwright.dev/python/) (`pytest-playwright`), Page Object Model
- **Test runner:** `pytest`, with custom markers: `smoke`, `functional`, `regression`, `negative`, `api`, `mobile`
- **API testing:** `requests` + `pytest`
- **Test data:** `Faker`, generating unique emails/names per run (this is a shared public site)
- **Reporting:** Allure (`allure-pytest`) + `pytest-html`
- **CI/CD:** GitHub Actions (core) + a documented `Jenkinsfile` (stretch)

## Folder structure

```
├── .github/workflows/ci.yml   # GitHub Actions: cross-browser matrix, nightly regression, report publish
├── pages/                     # Page Object Model — no raw locators inside test files
│   ├── base_page.py           #   shared header nav (login/logout/cart/products links)
│   ├── home_page.py, login_page.py, signup_page.py
│   ├── products_page.py, product_details_page.py
│   ├── cart_page.py, checkout_page.py, contact_us_page.py
├── tests/
│   ├── ui/                    # Playwright UI tests (+ tests/ui/conftest.py for UI-only fixtures)
│   └── api/                   # requests-based API tests
├── utils/
│   ├── data_factory.py        # Faker-based unique test data
│   ├── api_client.py          # thin wrapper over the site's REST API
│   └── config.py              # base URL / env handling
├── docs/test_plan.md          # every test case: ID, type, priority, steps, expected result
├── conftest.py                # shared fixtures (registered_user via API)
├── pytest.ini, requirements.txt, Jenkinsfile, .env.example
```

## Setup + running locally

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
playwright install --with-deps    # downloads Chromium, Firefox, WebKit
```

Run the whole suite (default browser: Chromium):

```bash
pytest
```

Common variations:

```bash
pytest -m smoke                                  # fast smoke suite only
pytest -m "smoke or negative"                     # combine markers
pytest tests/api                                  # API tests only (no browser needed)
pytest --browser firefox --browser webkit          # cross-browser: repeat --browser per engine
pytest tests/ui/test_mobile.py                     # mobile-emulation tests (iPhone 13)
pytest --alluredir=reports/allure-results          # collect Allure results
pytest --html=reports/report.html --self-contained-html   # a single-file HTML report
```

To view an Allure report locally you need the [Allure commandline](https://allurereport.org/docs/install/) installed:

```bash
allure serve reports/allure-results
```

## CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main`, on a nightly cron, and on manual
dispatch:

- **Push/PR:** a fast `smoke + api` subset across Chromium, Firefox, and WebKit.
- **Nightly / manual:** the full `smoke + functional + regression + negative + api + mobile` suite, same 3-browser matrix.
- Every run uploads per-browser `pytest-html` and Allure results (and JUnit XML) as build
  artifacts, so a report is always reachable even if a step fails.
- On `main` (not on PRs), a separate job merges all browsers' Allure results and publishes the
  report to GitHub Pages — linked at the top of this README.

A `Jenkinsfile` is also included as a stretch goal, mirroring the same stages, for running this
suite on a local Jenkins instance (see the comments in the file for the Docker agent image and
Allure Commandline setup it expects).

## Test data & isolation

This is a shared public site, not a sandbox — other automated suites hit it too:

- Every registration/account uses a `Faker`-generated unique email (see `utils/data_factory.py`); nothing is hardcoded.
- Assertions target data *shape* and *behavior* (e.g. "at least one result", "these fields are present"), never exact product counts that could shift as the shared catalog changes.
- Tests are independent — no test relies on state left behind by another. Accounts created via the `registered_user` fixture are deleted again in teardown.

## Known limitations & next steps

Deliberate scope boundaries, not gaps someone forgot:

- **Appium / native mobile app testing** is out of scope — it needs a real app binary and
  emulator, a different project entirely. "Mobile" coverage here means Playwright's device
  emulation (viewport, touch, user agent), not a native app.
- **Performance testing** is a stretch goal only, not core scope (see the GitHub issues for a
  planned basic Locust/k6 smoke check).
- **A real TestRail/TestLink account** wasn't used — `docs/test_plan.md` documents test cases
  in the same structured way (ID, preconditions, steps, expected result, priority, type) as a
  deliberate, honest substitute for a paid TCM tool.
- Open, tracked improvements live in [GitHub Issues](https://github.com/DjoleBP/automationexercise-qa-framework/issues) — e.g. more checkout negative coverage, an Allure Commandline install step for the Jenkinsfile, Docker one-command setup, and visual regression baselines.

## Project tracking

Work is tracked with [GitHub Issues](https://github.com/DjoleBP/automationexercise-qa-framework/issues) and a [Project board](https://github.com/users/DjoleBP/projects) (To Do / In Progress / Done) — the GitHub-native stand-in for Jira/Trello for this project.
