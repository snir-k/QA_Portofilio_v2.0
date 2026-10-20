@echo off
:: QA AUTOMATION FRAMEWORK HUB - ENTERPRISE CONTROL ROOT
cls
echo Loading Core QA Framework Automation Central Control Center...
call .venv\Scripts\activate
python run_all_tests.py
if errorlevel 1 (
    echo [Critical Error] The Python central dashboard failed to load.
    pause
)
exit
