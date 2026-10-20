# app/services/cli_generator.py

from typing import Optional


class CLIGeneratorService:
    @staticmethod
    def generate_command(build_tool: Optional[str], framework: Optional[str], test_id: Optional[str] = None) -> str:
        """
        מחולל פקודות CLI מקצועיות להרצת בדיקות אוטומציה במסוף (Terminal).
        תומך בכלי בנייה (Maven/Gradle) ובספריות הרצה (TestNG/JUnit 5).
        מטפל בהגנת טיפוסים חסינה מפני ערכי None.
        """
        # הגנת שכבה והבטחת טיפוס מחרוזת נקי (Type Guarding)
        clean_build = str(build_tool).lower().strip() if build_tool else "maven"
        clean_framework = str(framework).lower().strip() if framework else "junit5"

        # בניית פקודת בסיס לפי כלי הפיתוח והבנייה (Build Tool)
        if clean_build == "maven":
            if test_id:
                # הרצת בדיקה ספציפית ב-Maven
                if clean_framework == "testng":
                    return f"mvn test -Dtest=*.*#{test_id} -DfailIfNoTests=false"
                else:  # junit5
                    return f"mvn test -Dtest={test_id}"
            return "mvn clean test"

        elif clean_build == "gradle":
            if test_id:
                # הרצת בדיקה ספציפית ב-Gradle
                if clean_framework == "testng":
                    return f"./gradlew test --tests \"*.*.{test_id}\""
                else:  # junit5
                    return f"./gradlew test --tests \"*{test_id}*\""
            return "./gradlew clean test"

        else:
            # ברירת מחדל חסינה במקרה של קלט לא צפוי
            return f"echo 'Unsupported build tool: {clean_build}'"
