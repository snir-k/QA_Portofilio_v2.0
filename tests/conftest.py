# tests/conftest.py

import os
import json
import pytest
from selenium import webdriver

# 🛡️ הגדרת הכתובת באמצעות חיבור מחרוזות מפורש למניעת חיתוכי אבטחה במסך!
BASE_URL = "http://127.0.0.1" + ":5000/"


@pytest.fixture(scope="function", autouse=True)
def init_and_reset_database():
    """
    🔄 פיקסטורה גלובלית מוגנת בהרצה אוטומטית בכל טסט בנפרד (scope="function").
    מאתחלת ומנקה את בסיס הנתונים המקומי למצבו המקורי לפני תחילת כל בדיקה.
    """
    base_dir = str(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, 'data.json')

    default_data = {
        "cms_settings": {
            "welcome_text": "שלום שניר! דאשבורד ניהול ואוטומציה (Full-Stack Python) 🚀"
        },
        "technologies": [
            {"name": "Python", "icon_path": "/static/assets/python-icon.png", "color": "#4B8BBE"},
            {"name": "Selenium", "icon_path": "/static/assets/selenium-icon.png", "color": "#32CD32"},
            {"name": "Flask", "icon_path": "/static/assets/flask-icon.png", "color": "#FFD700"},
            {"name": "PyCharm", "icon_path": "/static/assets/pycharm-icon.png", "color": "#21D4FD"},
            {"name": "Postman", "icon_path": "/static/assets/postman-icon.png", "color": "#FF6C37"},
            {"name": "GitHub", "icon_path": "/static/assets/github-icon.png", "color": "#FFFFFF"}
        ]
    }

    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pytest.fail(f"❌ נכשלה הכנת תשתית בסיס הנתונים ב-conftest: {e}")

    yield


@pytest.fixture(scope="function")
def driver():
    """
    🌐 פיקסטורה פונקציונלית המנהלת את מחזור החיים של Selenium WebDriver.
    מנווטת לכתובת הבסיס המעודכנת בפורט 5000 ומנקה את הדפדפן בסיום.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.implicitly_wait(3)
    chrome_driver.get(BASE_URL)

    yield chrome_driver

    chrome_driver.quit()
