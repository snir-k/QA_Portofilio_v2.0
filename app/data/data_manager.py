# app/data/data_manager.py

import os
import json


class DataManager:
    def __init__(self):
        # 📂 הגדרת נתיב פיזי קבוע לקובץ הנתונים בשורש הפרויקט
        base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.db_path = os.path.join(base_dir, 'data.json')

        # מערך בדיקות האוטומציה המקוריות (נשמר בזיכרון הריצה לריצה מהירה של טסטים)
        self._tests = [
            {"id": "TC-101", "name": "Verify Admin Login with Valid Credentials", "type": "UI", "severity": "Critical",
             "status": "Passed", "execution_time": 45, "coverage": 95, "stability": 100, "log": ""},
            {"id": "TC-102", "name": "Verify API Response for Dashboard Metrics", "type": "API", "severity": "Major",
             "status": "Passed", "execution_time": 12, "coverage": 88, "stability": 92, "log": ""},
            {"id": "TC-103", "name": "Validate CMS Technology Carousel Update", "type": "UI", "severity": "Medium",
             "status": "Failed", "execution_time": 68, "coverage": 75, "stability": 40,
             "log": "AssertionError: Expected text 'Python' but found 'React' at CSS selector #carouselItem-1"}
        ]

        # טעינת נתוני ה-CMS והטכנולוגיות מתוך הקובץ החסין
        self._load_from_file()

    def _load_from_file(self):
        """קריאת הנתונים מקובץ ה-JSON בטעינת השרת"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._cms_settings = data.get("cms_settings", {
                        "welcome_text": "שלום שניר! דאשבורד ניהול ואוטומציה (Full-Stack Python) 🚀"})
                    self._technologies = data.get("technologies", [])
                    return
            except Exception as e:
                print(f"[DATA ERROR] Failed to read JSON file, fallback to memory: {e}")

        # הגדרת ברירת מחדל חסינה במקרה שהקובץ חסר או פגום
        self._cms_settings = {"welcome_text": "שלום שניר! דאשבורד ניהול ואוטומציה (Full-Stack Python) 🚀"}
        self._technologies = [
            {"name": "Python", "icon_path": "/static/assets/python-icon.png", "color": "#4B8BBE"},
            {"name": "Selenium", "icon_path": "/static/assets/selenium-icon.png", "color": "#32CD32"}
        ]

    def _save_to_file(self):
        """שמירה פיזית של השינויים לקובץ ה-JSON"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "cms_settings": self._cms_settings,
                    "technologies": self._technologies
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[DATA ERROR] Failed to write JSON file: {e}")

    def get_all_tests(self):
        return self._tests

    def add_test(self, test_data):
        required_fields = ["id", "name", "type", "severity", "status", "execution_time", "coverage", "stability"]
        for field in required_fields:
            if field not in test_data:
                raise ValueError(f"Missing required field: {field}")
        self._tests.append(test_data)
        return True

    def get_cms_settings(self):
        return self._cms_settings

    def update_cms_settings(self, new_settings):
        if "welcome_text" in new_settings:
            self._cms_settings["welcome_text"] = str(new_settings["welcome_text"]).strip()
            self._save_to_file()  # שמירה לצמיתות
        return True

    def get_technologies(self):
        return self._technologies

    def add_technology(self, name, icon_path, color):
        name_clean = str(name).strip()
        if name_clean and not any(t["name"].lower() == name_clean.lower() for t in self._technologies):
            self._technologies.append({
                "name": name_clean,
                "icon_path": icon_path or "/static/assets/default-icon.png",
                "color": str(color).strip() or "#FFFFFF"
            })
            self._save_to_file()  # שמירה לצמיתות
            return True
        return False

    def delete_technology(self, name):
        name_clean = str(name).strip()
        for t in self._technologies:
            if t["name"] == name_clean:
                self._technologies.remove(t)
                self._save_to_file()  # שמירה לצמיתות
                return True
        return False

# app/data/data_manager.py

    def reload_data(self):
        """
        🔄 מתודה ציבורית רשמית (Public Method) לרענון הנתונים מהדיסק.
        מאפשרת לקבצים חיצוניים (כמו Routes) לבקש סנכרון בלייב מבלי לגשת לחברים מוגנים.
        """
        self._load_from_file()


db_manager = DataManager()
