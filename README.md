# Functional Testing, CI/CD Pipeline & Live Deployment

[![CI/CD Pipeline](https://github.com/TaniaAkterLima/functional-testing-2507207/actions/workflows/ci.yml/badge.svg)](https://github.com/TaniaAkterLima/functional-testing-2507207/actions/workflows/ci.yml)
[![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://github.com/TaniaAkterLima/functional-testing-2507207)
[![Coverage](https://img.shields.io/badge/coverage-100%25%20(line%20%26%20branch)-brightgreen.svg)](https://github.com/TaniaAkterLima/functional-testing-2507207)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- **Student ID**: `2507207`
- **Course**: Software Quality Assurance & Testing
- **Assignment**: Functional Testing, CI/CD and Live Deployment
- **Repository**: [https://github.com/TaniaAkterLima/functional-testing-2507207](https://github.com/TaniaAkterLima/functional-testing-2507207)
- **Live Deployment URL**: [https://functional-testing-2507207.onrender.com](https://functional-testing-2507207.onrender.com)
- **Live Health Endpoint**: [https://functional-testing-2507207.onrender.com/health](https://functional-testing-2507207.onrender.com/health)

---

## Table of Contents
1. [Overview](#overview)
2. [Local Setup & Installation](#local-setup--installation)
3. [Running Tests & Coverage](#running-tests--coverage)
4. [CI/CD Pipeline Architecture](#cicd-pipeline-architecture)
5. [Verified Red-to-Green CI Demonstrations](#verified-red-to-green-ci-demonstrations)
6. [Interactive Web Frontend](#interactive-web-frontend)
7. [Live Deployment & Smoke Tests](#live-deployment--smoke-tests)
8. [Suspected Bugs in target.py](#suspected-bugs-in-targetpy)
9. [Bonus Points Compliance](#bonus-points-compliance)

---

## Overview

This project implements a complete testing, automation, and continuous delivery pipeline for `target.py` (containing 16 functions: 11 data-type functions and 5 mathematical functions).

Per the assignment rules, **`target.py` has not been modified in any way**. All corner cases, boundaries, wrong types, and suspected bugs are thoroughly tested and documented below.

---

## Local Setup & Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git

### Steps
```bash
# 1. Clone repository
git clone https://github.com/TaniaAkterLima/functional-testing-2507207.git
cd functional-testing-2507207

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. Run Flask web application locally
python app.py
# Web app is accessible at: http://localhost:5000
```

---

## Running Tests & Coverage

To run the functional test suite and verify **100% line and branch coverage**:

```bash
# Run pytest with branch coverage enforcement
pytest --cov=target --cov-branch --cov-report=term-missing --cov-fail-under=100

# Run linting check
flake8 .
```

### Coverage Report Summary
```
Name        Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------
target.py      59      0     26      0   100%
-------------------------------------------------------
TOTAL          59      0     26      0   100%
```

All 181 functional tests in `tests/test_target.py` pass with **100% statement and branch coverage**. An additional 46 integration tests in `tests/test_app.py` verify the Flask API endpoints and web interface.

---

## CI/CD Pipeline Architecture

The workflow is defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and follows the pipeline design:

```
[ Push / PR to main ]
          │
          ▼
   [ test Job ] (Matrix: Python 3.10, 3.11, 3.12)
   ├── Pip Caching
   ├── Flake8 Linting
   ├── Pytest 100% Line & Branch Coverage Enforcement
   └── Coverage HTML Report Upload as Artifact
          │
          ├── [ Tests Fail ] ──> Pipeline Stops; Deploy is SKIPPED
          │
          ▼ [ All Tests Pass ]
   [ deploy Job ] (needs: test, pushes to main only)
   └── Triggers Render Deploy Webhook via GitHub Secret
          │
          ▼
   [ smoke-test Job ] (needs: deploy)
   ├── Polls /health until deployed commit SHA matches github.sha
   ├── Check 1: GET /health returns HTTP 200 and verified SHA
   ├── Check 2: POST /api/run factorial calculation returns 120
   └── Check 3: POST /api/run divide by zero returns HTTP 400
          │
          ▼
   [ Change Verified Live in Frontend Footer ]
```

---

## Verified Red-to-Green CI Demonstrations

As required by Part 3 of the assignment (*"Include one red run from a failing test, then a green fix"*):

1. **Red Run (Failing Test)**:
   - **Run URL**: [Actions Run #42476543376](https://github.com/TaniaAkterLima/functional-testing-2507207/actions/runs/42476543376)
   - **Commit**: `fc5f49d` (`ci: configure GitHub Actions test matrix with intentional failing test for red run`)
   - **Outcome**: **FAILED (Red)** — detected failing test assertion and prevented merging/deployment.
2. **Green Run (Fix Restored)**:
   - **Run URL**: [Actions Run #42476731353](https://github.com/TaniaAkterLima/functional-testing-2507207/actions/runs/42476731353)
   - **Commit**: `74bcc1c` (`fix(deps): pin cross-version dependencies supporting Python 3.10-3.12`)
   - **Outcome**: **SUCCESS (Green)** — all matrix jobs passed on Python 3.10, 3.11, and 3.12 with 100% coverage and artifact uploaded.

---

## Interactive Web Frontend

The web frontend (`app.py`, `templates/index.html`) provides an interactive interface to execute and inspect each of the 16 `target.py` functions:

- **11 Data Type Functions**: Integer, Float, String, Boolean, None/Optional, List, Dict, Tuple, Set, Date, Type Conversion.
- **5 Mathematics Functions**: Divide, Power, Square Root, Factorial, Average.
- **Dynamic Categories**: Filter cards by "All", "Data Types", or "Mathematics".
- **Visual Feedback**:
  - Green card alerts for successful returns with output type and formatted result.
  - Red card alerts displaying exact Python exception type and error message when invalid inputs are provided.
- **Live Footer**: Queries `/health` asynchronously and displays the active deployed commit SHA on the live page.

---

## Live Deployment & Smoke Tests

- **Platform**: Render Web Service
- **Auto-Deploy**: Disabled (manual webhook deploy only).
- **Deployment Hook**: Triggered by GitHub secret `RENDER_DEPLOY_HOOK_URL`.
- **Smoke Tests**:
  1. `GET /health` — verifies HTTP 200 and checks that `commit_sha` matches `github.sha`.
  2. `POST /api/run` — computes `factorial(5)` and asserts `result == 120`.
  3. `POST /api/run` — attempts `divide(10, 0)` and asserts HTTP 400 with `"cannot divide by zero"`.

---

## Suspected Bugs in target.py

In accordance with the instruction (*"Do not modify target.py; the original is restored at grading. Report suspected bugs in your README"*), the following bugs, inconsistencies, and edge-case design flaws were identified in `target.py`:

| # | Function | Suspected Bug / Vulnerability | Expected Behavior | Actual Behavior in `target.py` | Reproduction Case |
|---|---|---|---|---|---|
| 1 | `is_adult(age)` | Does not type-check booleans | Booleans should raise `TypeError` because age is a human year count. | Python's `bool` subclasses `int` (`True == 1`), so `is_adult(True)` evaluates `1 >= 18` and returns `False` instead of erroring. | `target.is_adult(True)` -> `False` |
| 2 | `greet(name=None)` | Unhandled `AttributeError` for non-string objects | Non-strings should raise `TypeError` or be stringified. | Directly calls `name.strip()`; non-string objects lack `.strip()`, crashing with unhandled `AttributeError`. | `target.greet(123)` -> `AttributeError: 'int' object has no attribute 'strip'` |
| 3 | `find_max(numbers)` | Does not enforce list type or comparable elements | Should raise `TypeError` if input is not a sequence of comparable numbers. | Allows tuples; lists containing unorderable types (e.g. `[1, "2"]`) crash with `TypeError: '>' not supported between instances...`. | `target.find_max([1, "two"])` -> `TypeError` |
| 4 | `swap(pair)` | Accepts any 2-element sequence instead of requiring a 2-tuple | Should validate `isinstance(pair, tuple)`. | Accepts 2-character strings or lists (e.g. `"ab"`), returning `('b', 'a')`. | `target.swap("ab")` -> `('b', 'a')` |
| 5 | `common_items(set_a, set_b)` | Uses bitwise `&` operator rather than `set.intersection()` | `set.intersection()` accepts any iterable. Bitwise `&` strictly requires both sides to be sets. | If `set_a` is a list, `list & set` crashes with `TypeError: unsupported operand type(s) for &`. | `target.common_items([1, 2], {2, 3})` -> `TypeError` |
| 6 | `is_leap_year(year)` | Does not validate integer type | Should enforce `isinstance(year, int)` since calendar years are integers. | Floats like `2024.0` pass modulo math. Booleans like `True` evaluate `1 >= 1` and return `False`. | `target.is_leap_year(2024.0)` -> `True` |
| 7 | `power(base, exponent)` | Produces complex numbers for negative base with fractional exponent | In standard real math, negative roots should raise `ValueError` unless complex math is explicitly intended. | `power(-4, 0.5)` returns `(1.22e-16+2j)` instead of raising `ValueError`. | `target.power(-4, 0.5)` -> `(1.22e-16+2j)` |
| 8 | `factorial(n)` | Does not validate integer `n` | Should enforce non-negative integer input. | Passing a float crashes with `TypeError: 'float' object cannot be interpreted as an integer` in `range()`. | `target.factorial(4.5)` -> `TypeError` |
| 9 | `to_int(value)` | Silently truncates floats | Should either round or reject non-integer strings/floats cleanly. | `to_int(5.9)` returns `5` silently, while string floats like `to_int("5.9")` raise `ValueError`. Inconsistent float handling. | `target.to_int(5.9)` -> `5`, `target.to_int("5.9")` -> `ValueError` |
| 10 | `divide(a, b)` | Does not validate numeric inputs | Non-numeric arguments should raise descriptive `TypeError`. | Calling `divide("10", 2)` raises `TypeError: unsupported operand type(s) for /: 'str' and 'int'`. | `target.divide("10", 2)` -> `TypeError` |

---

## Bonus Points Compliance

- **3+ Feature Branches Merged via Pull Requests (+1 bonus)**:
  - [PR #1](https://github.com/TaniaAkterLima/functional-testing-2507207/pull/1): `feature/part1-functional-tests` (Comprehensive test suite with 100% coverage).
  - [PR #2](https://github.com/TaniaAkterLima/functional-testing-2507207/pull/2): `feature/part3-ci-workflow` (GitHub Actions CI workflow matrix & Red-Green demonstration).
  - [PR #3](https://github.com/TaniaAkterLima/functional-testing-2507207/pull/3): `feature/part4-frontend-web` (Web frontend with interactive runner and live commit SHA).
  - [PR #4](https://github.com/TaniaAkterLima/functional-testing-2507207/pull/4): `feature/part5-deployment-pipeline` (Render deployment webhook trigger and automated smoke tests).
- **Branch Protection on `main` Requiring CI (+1 bonus)**:
  - Branch protection is active on branch `main`.
  - Required status checks: `test (3.10)`, `test (3.11)`, `test (3.12)`.
  - Verified via GitHub API branch protection settings.
