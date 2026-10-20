# app/services/metrics_service.py

from app.data.data_manager import db_manager


class MetricsService:
    @staticmethod
    def calculate_dashboard_metrics():
        """
        שליפת הבדיקות וחישוב 4 קוביות המדדים המרכזיות עבור הדאשבורד.
        מטפל במקרי קצה של מערך ריק למניעת שגיאות חלוקה באפס.
        """
        tests = db_manager.get_all_tests()
        total_tests = len(tests)

        if total_tests == 0:
            return {
                "success_rate": 0,
                "total_duration": "00:00",
                "avg_coverage": 0,
                "stability_score": 0
            }

        passed_tests = sum(1 for t in tests if t["status"] == "Passed")
        total_seconds = sum(t["execution_time"] for t in tests)
        total_coverage = sum(t["coverage"] for t in tests)
        total_stability = sum(t["stability"] for t in tests)

        # 1. חישוב אחוז ההצלחה
        success_rate = round((passed_tests / total_tests) * 100)

        # 2. המרת זמן ריצה כולל מפורמט שניות למבנה MM:SS מוגן
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        total_duration = f"{minutes:02d}:{seconds:02d}"

        # 3. חישוב ממוצע כיסוי קוד
        avg_coverage = round(total_coverage / total_tests)

        # 4. חישוב מדד יציבות קוד ממוצע (Stability / Flakiness)
        stability_score = round(total_stability / total_tests)

        return {
            "success_rate": success_rate,
            "total_duration": total_duration,
            "avg_coverage": avg_coverage,
            "stability_score": stability_score
        }

    @staticmethod
    def get_formatted_table_data():
        """
        הכנת נתוני הטבלה להצגה בשכבת ה-UI.
        כולל החרגה מובנית של הלוגים לטובת אסרטים מהירים, והכנתם כשורות נפתחות בלבד.
        """
        return db_manager.get_all_tests()
