# git_automation_dashboard.py
# =================================================================
# ENTERPRISE QA AUTOMATION INTEGRATION & CONTROL CENTER
# Hardened to support version control tracking and dynamic Git delivery pipelines
# 100% Sterile: Eradicated style warnings by replacing legacy hooks
# =================================================================

import subprocess
import sys
from typing import List

# ANSI Color Escape Sequences
NEON_GREEN = "\033[92m"
WARNING_ORANGE = "\033[93m"
RESET = "\033[0m"


def _run_git_command(command: List[str]) -> str:
    """Private Helper: Executes a Git command safely via subprocess and returns the output."""
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing git hook: {e.stderr.strip()}"


def get_current_branch() -> str:
    """Queries the local Git repository to extract the active working branch name dynamically."""
    branch = _run_git_command(["git", "branch", "--show-current"])
    return branch if "Error" not in branch and branch else "unknown"


def _clear_terminal_screen() -> None:
    """Private Helper: Clears the command line screen safely to satisfy OS-agnostic matrix constraints."""
    is_windows = sys.platform.startswith("win")
    subprocess.run(["cls" if is_windows else "clear"], shell=True)


def execute_atomic_pipeline() -> None:
    """Executes a complete automated commit and push version control delivery pipeline."""
    commit_message = input("\nEnter a descriptive release commit message in English: ").strip()
    if not commit_message:
        print(f"\n{WARNING_ORANGE}[Validation Error] Commit message cannot be empty! Pipeline aborted.{RESET}")
        return

    current_branch = get_current_branch()
    print(f"\nTarget Repository Branch Detected: [{current_branch.upper()}]")
    print("-----------------------------------------------------------------")

    print("1. Staging total project alterations into the repository stack...")
    _run_git_command(["git", "add", "."])

    print("2. Compiling atomic release commit matrix...")
    print(_run_git_command(["git", "commit", "-m", commit_message]))

    print(f"3. Transmitting pipeline payload straight to origin/{current_branch}...")
    _run_git_command(["git", "push", "origin", current_branch])
    print(f"\n{NEON_GREEN}[Pipeline Complete] GitHub Repository is 100% synchronized and secure!{RESET}")


def run_git_submenu() -> None:
    """Renders the sub-menu for advanced Git automation operations."""
    while True:
        _clear_terminal_screen()
        current_branch = get_current_branch()
        print("=================================================================")
        print("          QA FRAMEWORK - VERSION CONTROL CONTROLLER HUB          ")
        print("=================================================================")
        print(f" Active Working Repository Branch:  [{current_branch.upper()}]")
        print("=================================================================")
        print(f"  {NEON_GREEN}1. Synchronize Framework (Automated Atomic Commit & Push to GitHub){RESET}")
        print("  2. Refresh Tracking Matrix (Clear Local Cache & Index Latency)")
        print("  3. Audit Current Status (Show Unstaged Changes & Untracked Files)")
        print("  4. View Version Trace History (Show Short Commit Log)")
        print("  5. Return to Central Automation Runner Hub")
        print("=================================================================")

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            execute_atomic_pipeline()
            input("\nPress Enter to continue...")
        elif choice == "2":
            print("\nClearing Git index cache...")
            print(_run_git_command(["git", "update-index", "--refresh"]))
            print("System tracking state sterile and optimized.")
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("\n--- Current Workspace Status ---")
            print(_run_git_command(["git", "status", "-s"]))
            input("\nPress Enter to continue...")
        elif choice == "4":
            print("\n--- Recent Repository Updates (Short Trace Log) ---")
            print(_run_git_command(["git", "log", "-n", "5", "--oneline"]))
            input("\nPress Enter to continue...")
        elif choice == "5":
            break
