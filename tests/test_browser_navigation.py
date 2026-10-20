# tests/test_browser_navigation.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.positive
@pytest.mark.xray("QA-201")
def test_failed_test_row_log_accordion_toggle(driver):
    """
    🧪 תרחיש פונקציונלי: אימות מנגנון פתיחה וסגירה דינמית של שורות הלוג (Stack Trace) בטבלה.
    מוודא שבלחיצה על טסט שנכשל (TC-103) שורת הלוג נפתחת, ובלחיצה נוספת נסגרת.
    משתמש בעוגן מזהה קשיח וחסין מפני שינויי מחלקות CSS של מפתחים.
    """
    wait = WebDriverWait(driver, 10)

    # 1. איתור שורת הטסט לפי עוגן מזהה ייחודי בלבד (חסין מפני שינויי אותיות גדולות/קטנות בסטטוס)
    failed_row = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "tr.test-row[data-id='TC-103']")))

    # וידוא פנימי שהשורה אכן מייצגת בדיקה שנכשלה לפני תחילת הבדיקה
    row_classes_lower = str(failed_row.get_attribute("class")).lower()
    assert "failed" in row_classes_lower, "❌ הבדיקה שנבחרה TC-103 אינה במצב Failed כפי שצפוי בבסיס הנתונים"

    # 2. איתור שורת הלוג המתאימה לה (מוודא שהיא קיימת ב-DOM אך מוסתרת כברירת מחדל ב-CSS)
    log_row = driver.find_element(By.CSS_SELECTOR, "tr.log-row[data-for='TC-103']")
    assert not log_row.is_displayed(), "❌ שורת הלוג הופיעה ויזואלית במסך לפני שבוצעה לחיצה"

    # 3. לחיצה ראשונה - פתיחת האקורדיון בלייב באמצעות JS
    failed_row.click()
    wait.until(lambda d: log_row.is_displayed())
    assert log_row.is_displayed(), "❌ שורת הלוג לא נחשפה ויזואלית לאחר לחיצה על השורה שנכשלה"

    # הגנת טיפוסים חסינה (Type Guarding): המרה מפורשת ל-String ומעבר לאותיות קטנות
    row_classes_after = str(failed_row.get_attribute("class")).lower()
    assert "active-log-parent" in row_classes_after, "❌ מחלקת העיצוב active-log-parent לא התווספה לשורה"

    # 4. לחיצה שנייה - סגירת האקורדיון והסתרת הלוג
    failed_row.click()
    wait.until(lambda d: not log_row.is_displayed())
    assert not log_row.is_displayed(), "❌ שורת הלוג נותרה גלויה לאחר לחיצה שנייה (האקורדיון לא נסגר)"


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.positive
@pytest.mark.xray("QA-202")
def test_table_row_count_resiliency_excluding_logs(driver):
    """
    🧪 תרחיש אבטחת טסט (Test Resiliency): הקשחת אסרטים מבוססי סלקטור חכם.
    מוודא שספירת הבדיקות הפעילות בטבלה מוחרגת משורות לוג שגיאה (tr:not(.log-row)),
    וכך מונע שבירת טסטים כאשר לוגים נפתחים או נסגרים ב-DOM.
    """
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.ID, "testTableBody")))

    active_rows = driver.find_elements(By.CSS_SELECTOR, "#testTableBody tr:not(.log-row)")
    assert len(active_rows) == 3, f"❌ ספירת השורות נכשלה. נמצאו {len(active_rows)} שורות במקום 3"


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.positive
@pytest.mark.xray("QA-203")
def test_obsidian_carousel_navigation_control(driver):
    """
    🧪 תרחיש ויזואלי ופונקציונלי: אימות מנגנון הניווט הידני של קרוסלת הטכנולוגיות.
    מוודא שלחיצה על לחצני הזכוכית אובסדיאן מעדכנת את מאפיין ה-transform של מסלול הקרוסלה.
    """
    wait = WebDriverWait(driver, 10)
    carousel_track = wait.until(ec.presence_of_element_located((By.ID, "carouselTrack")))
    next_btn = driver.find_element(By.ID, "nextTechBtn")

    initial_transform = carousel_track.value_of_css_property("transform")
    next_btn.click()

    wait.until(lambda d: carousel_track.value_of_css_property("transform") != initial_transform)
    updated_transform = carousel_track.value_of_css_property("transform")

    assert updated_transform != "none" and "matrix" in updated_transform, "❌ קרוסלת הטכנולוגיות לא זזה"
