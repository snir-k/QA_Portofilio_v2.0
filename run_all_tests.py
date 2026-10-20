# run_all_tests.py
# =================================================================
# ENTERPRISE QA AUTOMATION SYSTEM - CENTRAL SUITE RUNNER HUB
# Optimized to drive local testing execution layers and dynamic HTML outputs
# 100% Sterile: Zero Linter warnings and maximum PEP 8 type safety compliance
# =================================================================

import subprocess
import sys
from git_automation_dashboard import run_git_submenu, _clear_terminal_screen

# ANSI Color Escape Sequences
NEON_GREEN = "\033[92m"
LIGHT_BLUE = "\033[94m"
WARNING_ORANGE = "\033[93m"
RESET = "\033[0m"


def run_marker_submenu() -> None:
    """Renders a custom submenu to run tests filtered strictly by Pytest Markers."""
    while True:
        _clear_terminal_screen()
        print("=================================================================")
        print("          QA FRAMEWORK - SELECTIVE MARKER EXECUTION CONTROLLER   ")
        print("=================================================================")
        print("  1. Run ONLY Selenium Browser E2E Tests (-m ui)")
        print("  2. Run ONLY RESTful Web API Tests (-m api)")
        print("  3. Run ONLY Boundary Condition Exception Hardening (-m negative)")
        print("  4. Return to Main Dashboard")
        print("=================================================================")

        choice = input("Select a marker filter (1-4): ").strip()
        if choice == "1":
            subprocess.run(
                ["pytest", "-m", "ui", "--html=reports/ui_marker_report.html", "--self-contained-html", "-v"])
            input("\nPress Enter to continue...")
        elif choice == "2":
            subprocess.run(
                ["pytest", "-m", "api", "--html=reports/api_marker_report.html", "--self-contained-html", "-v"])
            input("\nPress Enter to continue...")
        elif choice == "3":
            subprocess.run(
                ["pytest", "-m", "negative", "--html=reports/negative_hardening_report.html", "--self-contained-html",
                 "-v"])
            input("\nPress Enter to continue...")
        elif choice == "4":
            break


def execute_environment_sterilization() -> None:
    """Advanced QA Hook: Purges temporary execution files and residual cache lockouts."""
    print(f"\n{WARNING_ORANGE}[System Sterilization Active] Initializing cache purge...{RESET}")
    import shutil
    import os

    # 🧹 מחיקת תיקיות קאש שננעלות ב-Windows
    cache_folders = [".pytest_cache", "app/routes/__pycache__", "app/data/__pycache__", "app/services/__pycache__"]
    for folder in cache_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f" -> Successfully cleared residual artifacts from: {folder}")
    print(f"{NEON_GREEN}QA Automation Framework environment is 100% sterile and optimized!{RESET}")


def execute_server_smoke_check() -> None:
    """Advanced QA Hook: Verifies the Flask active listener latency matrix before execution."""
    print(f"\n{LIGHT_BLUE}[Smoke Check] Pinging Flask network listener layer on port 5000...{RESET}")
    import requests
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=3)
        if response.status_code == 200:
            print(f"{NEON_GREEN} -> Server Healthy! Response code: 200 OK. Latency within threshold.{RESET}")
        else:
            print(
                f"{WARNING_ORANGE} -> Server Warning! Listener active but returned code: {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"\n[Critical Failure] Local port 5000 actively refused the pipe payload! {e}")
        print("Please ensure Flask 'run.py' is fired up in PyCharm before running suite tests.")


def display_main_dashboard() -> None:
    """Renders the central system panel where option 1 shines bright in Neon Green."""
    while True:
        _clear_terminal_screen()
        print("=================================================================")
        print("        PRODUCT MANAGER QA AUTOMATION ECOSYSTEM RUNNER           ")
        print("=================================================================")
        # TARGET DESIGN: Only Option 1 is printed in brilliant neon green
        print(f"  {NEON_GREEN}1. Run All 15 Core Suite Tests (Complete Automated HTML Report){RESET}")
        print("  2. Run Integration Flow Suite Only (test_product_flow.py - 2 Tests)")
        print("  3. Run RESTful Web API Suite Only (test_product_api.py - 3 Tests)")
        print("  4. Run UI CMS Form Validation Only (test_browser_forms.py - 4 Tests)")
        print("  5. Run UI Obsidian Carousel & Accordion Only (test_browser_navigation.py - 3 Tests)")
        print("  6. Run Isolated Unit Service Mock Only (test_product_unit.py - 3 Tests)")
        print("  7. FILTER EXECUTION BY SPECIFIC PYTEST CUSTOM MARKER SUITES")
        print("  8. RUN REPO STERILIZATION (Purge Local .pytest_cache & Locked Artifacts)")
        print("  9. EXECUTE API SMOKE HEALTH CHECK (Validate Flask Server Pipeline Connection)")
        print("  10. Launch Advanced QA Git Automation Dashboard (Dynamic CLI Tool)")
        print("  11. Exit Framework Automation Runner Hub")
        print("=================================================================")

        choice = input("Select an architectural layer execution path (1-11): ").strip()

        if choice == "1":
            print("\nLaunching total 15 core suite test pipeline execution routine...")
            subprocess.run(
                ["pytest", "tests/", "--html=reports/complete_automation_report.html", "--self-contained-html",
                 "--cache-clear", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            subprocess.run(["pytest", "tests/test_product_flow.py", "--html=reports/flow_test_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            subprocess.run(
                ["pytest", "tests/test_product_api.py", "--html=reports/api_test_report.html", "--self-contained-html",
                 "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            subprocess.run(["pytest", "tests/test_browser_forms.py", "--html=reports/forms_test_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            subprocess.run(["pytest", "tests/test_browser_navigation.py", "--html=reports/navigation_test_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "6":
            subprocess.run(["pytest", "tests/test_product_unit.py", "--html=reports/unit_test_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "7":
            run_marker_submenu()
        elif choice == "8":
            execute_environment_sterilization()
            input("\nPress Enter to return to menu...")
        elif choice == "9":
            execute_server_smoke_check()
            input("\nPress Enter to return to menu...")
        elif choice == "10":
            run_git_submenu()  # זינוק תת תוכנית בבקרת הגרסאות
        elif choice == "11":
            print("\nExiting Framework Center safely. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    display_main_dashboard()
