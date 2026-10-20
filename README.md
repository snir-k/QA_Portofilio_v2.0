# 📊 Automation Testing Analytic Dashboard Framework v2.0

## 💎 Project Overview
This repository contains a comprehensive, enterprise-grade automated testing suite and dynamic management framework for our multi-tiered **Analytic Automation Dashboard**. The system is built utilizing **Python 3.14, Flask, Pytest, and Selenium WebDriver**. 

The framework features strict transactional test isolation, advanced metadata reporting, runtime monkey-patching, and persistent file synchronization layer to guarantee a flawless **100% test execution stability rate** under strict non-destructive continuous integration constraints.

---

## 📈 Quality Metrics & System Maturity
* **Development Pipeline:** Sprint 2 (v2.0) Production Release.
* **Defect Status:** **0 Active Bugs Remaining** (All legacy vulnerabilities hardened).
* **Code Quality Verification:** 0 Static Linter Warnings | 100% Sterile Project Workspace.
* **Automation Stability:** 15 Comprehensive E2E, API, and Unit Iterations compiled successfully with a 100% Pass Rate.

---

## 🧪 Complete Automated Testing Scope

The execution layer enforces rigorous programmatic validation bounds distributed across 5 decoupled automated engine testing files. Use the links below to inspect the target code architecture directly:

| Target Layer Module | Component / Logic Under Test | Active Test Volume | Execution Profile & Drivers | Applied Project Markers |
| :--- | :--- | :---: | :--- | :--- |
| [🔹 tests/test_product_flow.py](#-test_product_flowpy) | Live simulation hooks, async spinner element degradation, and real-time Chart.js graph synchronizations. | **2 Passed** | Selenium E2E Web Viewports & Lambda Predicates | `ui`, `positive`, `navigation`, `xray` |
| [🔹 tests/test_product_api.py](#-test_product_apipy) | Bare-metal HTTP client JSON payload processing, validation hardening, and memory-safe monkey patching. | **3 Passed** | Native Flask Route Clients & Runtime Dict Seeding | `api`, `positive`, `negative`, `xray` |
| [🔹 tests/test_browser_forms.py](#-test_browser_formspy) | Security form authentication fields, visibility icons, element offset verification, and duplicate input submission walls. | **4 Passed** | Selenium Web Drivers (Chrome) & WebDriverWait Gates | `ui`, `positive`, `negative`, `xray` |
| [🔹 tests/test_browser_navigation.py](#-test_browser_navigationpy) | Asynchronous log accordion expansion, error stack trace elements visibility, and manual Obsidian control nodes tracking. | **3 Passed** | Selenium Fluent Conditions & Non-Destructive Locators | `ui`, `navigation`, `positive`, `xray` |
| [🔹 tests/test_product_unit.py](#-test_product_unitpy) | Isolated analytical business logic layer execution, math limit boundaries, and zero-division guard check blocks. | **3 Passed** | Pure Isolated Logical Pipelines (Zero-Browser) | `unit`, `service`, `positive`, `xray` |

---

## 🛠️ Individual Test Suite Specifications

### 🔹 `tests/test_product_flow.py`
* **`test_e2e_live_simulation_trigger_and_charts_sync`:** Intercepts the dynamic simulation trigger event, monitors full spinner text element degradation under 1.5-second runtime thresholds, and asserts live structural grid updates.
* **`test_e2e_jira_search_filter_and_pie_chart_sync`:** Drives character stream injection matching lower-case criteria, validates zero-lag filter operations, and extracts structural IDs directly from table cell data structures to bypass rendering latency.

### 🔹 `tests/test_product_api.py`
* **`test_get_all_tests_api_happy_path`:** Targets network endpoints using clean HTTP methods to verify schema contracts and mandatory object keys.
* **`test_add_test_api_validation_hardening`:** Asserts core API safety and input validation boundaries by injecting malformed payloads to force proper client-side 400 error codes.
* **`test_metrics_service_business_logic_via_mock`:** Deploys memory-safe lambda patching to substitute dependencies with isolated data models, tracking mathematical rounding accuracy and HH:MM formatting rules.

### 🔹 `tests/test_browser_forms.py`
* **`test_admin_login_happy_path`:** Exercises standard workspace login credentials, verifies structural visibility updates, and ensures administrative panel deployment.
* **`test_admin_login_negative_invalid_password`:** Validates client-side data hardening limits by checking element resets and failure alert blocks upon corrupted payload input.
* **`test_admin_password_padding_and_visibility_toggle`:** Verifies layout consistency and CSS protection. Asserts that the password input padding is locked on 48px to prevent text collisions, and toggles type attributes (`password` to `text`) smoothly.
* **`test_admin_login_submit_via_enter_key`:** Bypasses UI element interaction loops by firing keydown submit hooks straight to the field to assess application workflow reactivity.

### 🔹 `tests/test_browser_navigation.py`
* **`test_failed_test_row_log_accordion_toggle`:** Validates interactive accordion containers by tracing the toggle state of dense trace elements when an explicit test row error occurs.
* **`test_table_row_count_resiliency_excluding_logs`:** Protects structural validation criteria by binding the explicit selector constraint `tr:not(.log-row)`, ensuring layout changes do not compromise core element counts.
* **`test_obsidian_carousel_navigation_control`:** Audits manual tracking parameters by clicking glass obsidian nodes and checking responsive translation vectors on the layout axis.

### 🔹 `tests/test_product_unit.py`
* **`test_metrics_calculation_success_rate_edge_cases`:** Hardens core business processing logic by throwing empty structures into calculation layers to verify graceful zero-division error handling.
* **`test_duration_formatter_seconds_to_string_via_service`:** Validates formatting abstractions by passing boundary intervals to confirm safe translation into time string tokens.
* **`test_metrics_calculation_averages_logic_via_service`:** Tests data matrix reduction layers to ensure accuracy in tracking coverage ratios and score rounding boundaries.

---

## 💻 Local Testing & Execution Environment

### Deployment Prerequisites
Ensure your local environment configuration satisfies the dependencies specified inside `pyproject.toml`:
* `pytest >= 8.0.0`
* `pytest-html >= 4.2.0`
* `selenium >= 4.20.0`
* `requests >= 2.32.3`

### Step-by-Step Deployment Routine
1. **Fire up the centralized Flask application server engine (Keep alive in background):**
   ```bash
   python run.py
   ```
2. **Launch the centralized local testing suite console panel by executing our automation batch wrapper:**
   ```text
   run_all_tests.bat
   ```
3. **Select Execution Route Layer:** To compile all 15 core suite test cases simultaneously and build the compiled visual dashboard report, choose option `1`. To perform a rapid listener ping check, select option `9`.
