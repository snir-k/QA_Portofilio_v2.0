# app/routes/dashboard.py

import random
import time
import json
from flask import Blueprint, render_template, jsonify, request
from app.services.metrics_service import MetricsService
from app.data.data_manager import db_manager

# הגדרת ה-Blueprint עבור מודול הדאשבורד והאנליטיקה
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def display_dashboard():
    """נתיב התצוגה הראשי של הדאשבורד - UI Layer"""
    db_manager.reload_data()
    metrics = MetricsService.calculate_dashboard_metrics()
    tests = MetricsService.get_formatted_table_data()
    cms_data = db_manager.get_cms_settings()
    tech_data = db_manager.get_technologies()

    return render_template(
        'index.html',
        status="Python Backend Active",
        metrics=metrics,
        tests=tests,
        cms=cms_data,
        technologies=tech_data
    )


@dashboard_bp.route('/api/tests', methods=['GET'])
def get_tests_api():
    """Endpoint רשמי לקבלת כל הטסטים בפורמט JSON נקי עבור הגרפים והטבלה"""
    db_manager.reload_data()
    tests = db_manager.get_all_tests()
    return jsonify(tests), 200


@dashboard_bp.route('/api/tests/add', methods=['POST'])
def add_test_api():
    """Endpoint מאובטח להוספת טסט חדש עם בדיקת תקינות שדות חובה"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        db_manager.add_test(data)
        return jsonify({"message": "Test cases added successfully", "id": data.get("id")}), 201

    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except RuntimeError:
        return jsonify({"error": "Internal Server Error"}), 500


@dashboard_bp.route('/api/tests/search', methods=['GET'])
def search_tests_api():
    """מערכת חיפוש חכמה מבוססת קטגוריה ושאילתה דינמית"""
    category = request.args.get('category', 'name').lower().strip()
    query = request.args.get('query', '').lower().strip()

    db_manager.reload_data()
    all_tests = db_manager.get_all_tests()

    if not query:
        return jsonify(all_tests), 200

    filtered_tests = []
    for test in all_tests:
        field_value = str(test.get(category, '')).lower().strip()
        if query in field_value:
            filtered_tests.append(test)

    return jsonify(filtered_tests), 200


@dashboard_bp.route('/api/simulation/run', methods=['POST'])
def run_simulation_api():
    """Endpoint המריץ סימולציית בדיקות אוטומציה חיה בצד השרת"""
    try:
        time.sleep(1.5)  # השהיית ריצה בשביל ה-Spinner ב-UI
        db_manager.reload_data()
        all_tests = db_manager.get_all_tests()

        for test in all_tests:
            test["execution_time"] = max(5, test["execution_time"] + random.randint(-10, 10))
            if test["id"] == "TC-103":
                if random.choice([True, False]):
                    test["status"] = "Passed"
                    test["log"] = ""
                    test["stability"] = 100
                else:
                    test["status"] = "Failed"
                    test[
                        "log"] = "AssertionError: Expected text 'Python' but found 'React' at CSS selector #carouselItem-1"
                    test["stability"] = 40

        # שמירת השינויים הדינמיים לתוך קובץ ה-JSON בארכיטקטורה חסינה
        try:
            with open(db_manager.db_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "cms_settings": db_manager.get_cms_settings(),
                    "technologies": db_manager.get_technologies()
                }, f, ensure_ascii=False, indent=2)
        except OSError as os_err:
            # תפיסה ממוקדת של שגיאות דיסק מעלימה את אזהרת Too broad exception clause
            print(f"[SIMULATION WRITE ERROR] Failed to persist temporary state: {os_err}")

        return jsonify({"status": "success", "tests": all_tests}), 200

    except RuntimeError:
        # סגירה תקינה וחוקית של ה-try העליון בפונקציה ללא שגיאות סינטקס
        return jsonify({"error": "Internal Server Error during simulation sequence"}), 500
