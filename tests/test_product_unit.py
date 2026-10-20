# tests/test_product_unit.py

import pytest
from app.services.metrics_service import MetricsService
from app.data.data_manager import db_manager


@pytest.mark.unit
@pytest.mark.service
@pytest.mark.positive
@pytest.mark.xray("QA-501")
def test_metrics_calculation_success_rate_edge_cases():
    """
    🧪 בדיקת יחידה: וידוא חסינות חישוב אחוז ההצלחה במקרי קצה של ערכים ריקים.
    מנצל Monkey Patching נקי כדי להזרים מערך בדיקות ריק לשכבת ה-Service,
    ומוודא שהמערכת מחזירה 0% בצורה מאובטחת ללא קריסה של חלוקה באפס.
    """
    empty_test_suite = []

    # שמירת הפונקציה המקורית לצורך שחזור (Tear-down)
    original_get_all_tests = db_manager.get_all_tests

    try:
        # דריסת המתודה בפונקציית למדא שמחזירה מערך ריק - חסין מאזהרות Linter!
        db_manager.get_all_tests = lambda: empty_test_suite

        # הרצה של המתודה הציבורית הרשמית של ה-Service
        calculated_metrics = MetricsService.calculate_dashboard_metrics()

        # אימות חסינות מקרה הקצה
        assert calculated_metrics[
                   "success_rate"] == 0, f"❌ חישוב מערך ריק נכשל. התקבל {calculated_metrics['success_rate']}%"
        assert calculated_metrics[
                   "total_duration"] == "00:00", f"❌ פורמט זמן ריקה שגוי: {calculated_metrics['total_duration']}"
        assert calculated_metrics["avg_coverage"] == 0
        assert calculated_metrics["stability_score"] == 0

    finally:
        # שחזור פונקציית המקור
        db_manager.get_all_tests = original_get_all_tests


@pytest.mark.unit
@pytest.mark.service
@pytest.mark.positive
@pytest.mark.xray("QA-502")
def test_duration_formatter_seconds_to_string_via_service():
    """
    🧪 בדיקת יחידה: אימות תקינות מנגנון המרת פורמט הזמן משניות למחרוזת MM:SS.
    בודק את ההמרה של 125 שניות החוצות את רף הדקה (צריך להפוך ל-02:05) דרך ה-Service הציבורי.
    """
    sample_suite = [
        {"id": "TC-1", "execution_time": 125, "coverage": 100, "stability": 100, "status": "Passed"}
    ]

    original_get_all_tests = db_manager.get_all_tests
    try:
        db_manager.get_all_tests = lambda: sample_suite
        calculated_metrics = MetricsService.calculate_dashboard_metrics()

        # 125 שניות צריכות להפוך בדיוק לפורמט מחרוזת של "02:05" (שתי דקות ו-5 שניות)
        assert calculated_metrics[
                   "total_duration"] == "02:05", f"❌ המרת פורמט הזמן נכשלה: {calculated_metrics['total_duration']}"
    finally:
        db_manager.get_all_tests = original_get_all_tests


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.xray("QA-503")
def test_metrics_calculation_averages_logic_via_service():
    """
    🧪 בדיקת יחידה: אימות חישוב הממוצעים של מדדי כיסוי הקוד והיציבות.
    מזרים ערכים מגוונים ומודד שהתוצאה המתקבלת בשכבת ה-Service הציבורית מדויקת ומעוגלת.
    """
    sample_suite = [
        {"id": "TC-1", "coverage": 90, "stability": 80, "status": "Passed", "execution_time": 10},
        {"id": "TC-2", "coverage": 80, "stability": 70, "status": "Passed", "execution_time": 20},
        {"id": "TC-3", "coverage": 70, "stability": 60, "status": "Failed", "execution_time": 30}
    ]

    # חישוב ידני צפוי לכיסוי קוד: (90 + 80 + 70) / 3 = 80%
    # חישוב ידני צפוי ליציבות: (80 + 70 + 60) / 3 = 70%

    original_get_all_tests = db_manager.get_all_tests
    try:
        db_manager.get_all_tests = lambda: sample_suite
        calculated_metrics = MetricsService.calculate_dashboard_metrics()

        assert calculated_metrics[
                   "avg_coverage"] == 80, f"❌ חישוב ממוצע כיסוי הקוד שגוי: {calculated_metrics['avg_coverage']}%"
        assert calculated_metrics[
                   "stability_score"] == 70, f"❌ חישוב ממוצע מדד היציבות שגוי: {calculated_metrics['stability_score']}%"
        # אחוז הצלחה: 2 מתוך 3 עברו -> 66.66% מעוגל ל-67%
        assert calculated_metrics[
                   "success_rate"] == 67, f"❌ חישוב אחוז ההצלחה המעוגל שגוי: {calculated_metrics['success_rate']}%"
    finally:
        db_manager.get_all_tests = original_get_all_tests
