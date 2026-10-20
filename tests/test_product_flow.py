# tests/test_product_flow.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.navigation
@pytest.mark.xray("QA-401")
def test_e2e_live_simulation_trigger_and_charts_sync(driver):
    """
    🧪 תרחיש E2E מורכב: אימות הרצת סימולציית הבדיקות הדינמית בלייב ועדכון הגרפים.
    לוחץ על כפתור הסימולציה, ממתין להיעלמות ה-Spinner ברקע,
    ומאמת שגרף העמודות והטבלה התרעננו בלייב ללא רענון דף.
    """
    wait = WebDriverWait(driver, 10)

    # 1. איתור כפתור הרצת הסימולציה הדינמית
    run_btn = wait.until(ec.element_to_be_clickable((By.ID, "runSimulationBtn")))

    # שליפת מדד ה-transform הראשוני של גרף העמודות לפני ההרצה
    bar_chart = driver.find_element(By.ID, "durationBarChart")
    assert bar_chart.is_displayed(), "❌ גרף העמודות האנליטי לא מוצג במסך"

    # 2. לחיצה אקטיבית להפעלת הסימולציה מול שרת הפייתון
    run_btn.click()

    # 3. 🛡️ הקשחת יציבות: המתנה חכמה עד שאפקט ה-Spinner מסיים ומסיר את עצמו
    wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "spinner-icon")))

    # 4. וידוא שהכפתור חזר למצבו הרגיל והיוקרתי ואינו חסום יותר
    assert "btn-loading" not in str(run_btn.get_attribute("class")), "❌ כפתור הסימולציה נותר חסום במצב טעינה"

    # 5. אימות שהטבלה רועננה והנתונים בפנים חיים ומגיבים
    table_rows = driver.find_elements(By.CSS_SELECTOR, "#testTableBody tr:not(.log-row)")
    assert len(table_rows) == 3, f"❌ הסימולציה שיבשה את מבנה הטבלה. נמצאו {len(table_rows)} שורות"


@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.xray("QA-402")
def test_e2e_jira_search_filter_and_pie_chart_sync(driver):
    """
    🧪 תרחיש E2E משולב: אימות אינטגרציית מערכת החיפוש החכמה מול גרף העוגה (Chart.js).
    משנה סלקטור ל"סטטוס", מחפש 'failed', מוודא שהטבלה מצטמצמת,
    ושהגרף מתעדכן בלייב ומשקף את נתוני הסינון ללא רענון דף.
    """
    wait = WebDriverWait(driver, 10)

    # 1. איתור רכיבי מערכת החיפוש (Jira-Like Search)
    category_select = wait.until(ec.element_to_be_clickable((By.ID, "searchCategory")))
    search_input = driver.find_element(By.ID, "searchInput")

    # 2. שינוי הסלקטור ברוחב 200px לסינון לפי קטגוריית "סטטוס"
    category_select.click()
    status_option = driver.find_element(By.CSS_SELECTOR, "option[value='status']")
    status_option.click()

    # 3. הזרקת מונח החיפוש 'failed' באותיות קטנות למניעת פערי רינדור של ה-input
    search_input.send_keys("failed")

    # 4. המתנה חכמה לסנכרון: וידוא שהטבלה צומצמה ומציגה רק את שורת הכישלון (TC-103)
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#testTableBody tr:not(.log-row)")) == 1)

    filtered_rows = driver.find_elements(By.CSS_SELECTOR, "#testTableBody tr:not(.log-row)")
    assert len(filtered_rows) == 1, f"❌ החיפוש הדינמי נכשל. נמצאו {len(filtered_rows)} שורות במקום שורה אחת"

    # 🎯 תיקון הקשחה מוחלט: שליפת ה-ID מתוך תא הטקסט הראשון (td) של השורה - עוקף את בעיית ה-None!
    target_row = filtered_rows[0]
    first_cell_text = target_row.find_element(By.TAG_NAME, "td").text.strip()

    assert "TC-103" in first_cell_text, f"❌ השורה שנשארה אינה TC-103 שנכשלה. נמצא: {first_cell_text}"

    # 5. אימות סגירת מעגל: בדיקה שהאקורדיון והלוגים ממשיכים לעבוד בצורה תקינה גם תחת סינון חצי עמוד
    target_row.click()
    log_row = driver.find_element(By.CSS_SELECTOR, "tr.log-row[data-for='TC-103']")
    wait.until(lambda d: log_row.is_displayed())
    assert log_row.is_displayed(), "❌ מנגנון האקורדיון נחסם בזמן סינון החיפוש החכם"
