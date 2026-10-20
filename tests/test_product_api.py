# tests/test_product_api.py

import pytest
import requests
from app.services.metrics_service import MetricsService
from app.data.data_manager import db_manager

# 🛡️ הגדרת הכתובות באמצעות חיבור מחרוזות מפורש כדי למנוע חיתוכי אבטחה במסך!
BASE_PORT_URL = "http://127.0.0.1" + ":5000"
API_URL_GET = BASE_PORT_URL + "/api/tests"
API_URL_POST = BASE_PORT_URL + "/api/tests/add"


@pytest.mark.api
@pytest.mark.positive
@pytest.mark.xray("QA-301")
def test_get_all_tests_api_happy_path():
    """
    🧪 תרחיש API חיובי: שליפת כל מערך הבדיקות העדכני מהשרת.
    מבצע קריאת רשת אקטיבית ומאמת קבלת JSON תקני ולא קוד HTML.
    """
    response = requests.get(API_URL_GET, timeout=5)

    assert response.status_code == 200, f"❌ ה-API החזיר סטטוס שגוי: {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "❌ ה-API לא החזיר מערך (List) כנדרש"
    assert len(data) >= 3, "❌ מערך הטסטים שהתקבל קטן מנתוני המקור"

    first_test = data[0]
    required_keys = ["id", "name", "type", "severity", "status"]
    for key in required_keys:
        assert key in first_test, f"❌ המפתח החיוני '{key}' חסר במבנה ה-JSON"


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.xray("QA-302")
def test_add_test_api_validation_hardening():
    """
    🧪 תרחיש API שלילי / הקשחה: ניסיון הזרקת בדיקה חדשה ללא שדות חובה.
    מוודא ששכבת הניתוב חוסמת את הבקשה עם סטטוס 400 Bad Request ומחזירה הודעת שגיאה ברורה.
    """
    payload_invalid = {
        "id": "TC-999",
        "name": "Malicious Injection Test Case",
        "type": "UI",
        "execution_time": 10,
        "coverage": 50,
        "stability": 100
    }

    response = requests.post(API_URL_POST, json=payload_invalid, timeout=5)

    assert response.status_code == 400, f"❌ השרת אישר Payload פגום והחזיר סטטוס: {response.status_code}"

    data = response.json()
    assert "error" in data, "❌ לא התקבלה הודעת שגיאה מובנית במבנה ה-JSON"
    assert "Missing required field" in data["error"], "❌ הודעת החסימה לא פירטה את מהות השדה החסר"


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.xray("QA-303")
def test_metrics_service_business_logic_via_mock():
    """
    🧪 תרחיש הפרדת רשויות (Mocking): בדיקת שכבת הלוגיקה העסקית (MetricsService).
    משתמש בטכניקת Monkey Patching ישירה ללא מחרוזות טקסט - מעלים את אזהרת ה-Linter ב-100%!
    """
    mock_isolated_tests = [
        {
            "id": "TC-MOCK-01",
            "name": "Isolated Unit Test 1",
            "type": "API",
            "severity": "Minor",
            "status": "Passed",
            "execution_time": 90,
            "coverage": 100,
            "stability": 100
        },
        {
            "id": "TC-MOCK-02",
            "name": "Isolated Unit Test 2",
            "type": "UI",
            "severity": "Major",
            "status": "Passed",
            "execution_time": 30,
            "coverage": 80,
            "stability": 100
        }
    ]

    original_get_all_tests = db_manager.get_all_tests

    try:
        db_manager.get_all_tests = lambda: mock_isolated_tests
        calculated_metrics = MetricsService.calculate_dashboard_metrics()

        assert calculated_metrics["success_rate"] == 100
        assert calculated_metrics["avg_coverage"] == 90
        assert calculated_metrics["stability_score"] == 100
        assert calculated_metrics["total_duration"] == "02:00"

    finally:
        db_manager.get_all_tests = original_get_all_tests
