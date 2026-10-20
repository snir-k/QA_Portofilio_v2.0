# tests/test_browser_forms.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.xray("QA-101")
def test_admin_login_happy_path(driver):
    """
    🧪 תרחיש חיובי: התחברות מנהל מערכת עם סיסמה תקינה ופתיחת ה-CMS.
    משתמש במתודות רשמיות והמתנות חכמות כדי להבטיח יציבות טסטים מוחלטת.
    """
    wait = WebDriverWait(driver, 10)

    # 1. איתור ולחיצה על כפתור פתיחת מצב המנהל (OFF)
    toggle_btn = wait.until(ec.element_to_be_clickable((By.ID, "adminToggleBtn")))
    toggle_btn.click()

    # 2. וידוא פתיחת מודאל האבטחה והזנת הסיסמה התקינה
    password_input = wait.until(ec.element_to_be_clickable((By.ID, "adminPassword")))
    password_input.send_keys("admin123")

    # 3. לחיצה על כפתור אימות הכניסה
    submit_btn = driver.find_element(By.ID, "submitAuthBtn")
    submit_btn.click()

    # 4. אסרט הקשחה: וידוא שפאנל ה-CMS נחשף לעיני המנהל והסטטוס הפך ל-ON
    cms_panel = wait.until(ec.visibility_of_element_located((By.ID, "cmsPanel")))
    assert cms_panel.is_displayed(), "❌ פאנל ה-CMS לא נחשף לאחר הזנת סיסמה תקינה"
    assert "מצב מנהל: ON" in toggle_btn.text, "❌ כפתור הסטטוס לא השתנה ל-ON ירוק"


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.xray("QA-102")
def test_admin_login_negative_invalid_password(driver):
    """
    🧪 תרחיש שלילי: ניסיון התחברות עם סיסמה שגויה (Payload Hardening).
    מוודא שמוצגת הודעת שגיאה מתאימה, שהשדה מתנקה, ושה-CMS נשאר נעול וחסוי.
    """
    wait = WebDriverWait(driver, 10)

    # 1. פתיחת המודאל
    driver.find_element(By.ID, "adminToggleBtn").click()
    password_input = wait.until(ec.element_to_be_clickable((By.ID, "adminPassword")))

    # 2. הזנת סיסמה שגויה ולחיצה על כפתור האימות
    password_input.send_keys("wrong_password_999")
    driver.find_element(By.ID, "submitAuthBtn").click()

    # 3. אסרט הקשחה: וידוא הופעת הודעת השגיאה באדום
    error_msg = wait.until(ec.visibility_of_element_located((By.ID, "authErrorMessage")))
    assert error_msg.is_displayed(), "❌ הודעת השגיאה באדום לא הופיעה במסך"

    # 4. וידוא ששדה הסיסמה התנקה אוטומטית לצורך ניסיון נוסף وشמר על המיקוד
    assert password_input.get_attribute("value") == "", "❌ שדה הסיסמה לא התנקה לאחר כישלון האימות"

    # 5. וידוא שפאנל ה-CMS נותר חסוי לחלוטין
    cms_panel = driver.find_element(By.ID, "cmsPanel")
    assert not cms_panel.is_displayed(), "❌ פאנל ה-CMS נחשף למרות שהוזנה סיסמה שגויה!"


@pytest.mark.ui
@pytest.mark.edge
@pytest.mark.xray("QA-103")
def test_admin_password_padding_and_visibility_toggle(driver):
    """
    🧪 תרחיש קצה ויזואלי: בדיקת מנגנון הגנת ה-CSS וכפתור העין (👁️/🙈).
    מוודא הקשחת נגישות: החלפת טיפוס השדה, והזחת padding קשיחה של 48px למניעת דריסת טקסט.
    """
    wait = WebDriverWait(driver, 10)

    # 1. פתיחת המודאל ואיתור השדות
    driver.find_element(By.ID, "adminToggleBtn").click()
    password_input = wait.until(ec.element_to_be_clickable((By.ID, "adminPassword")))
    toggle_eye_btn = driver.find_element(By.ID, "togglePasswordBtn")

    # 2. וידוא אבטחה בסיסית: סוג השדה כברירת מחדל חייב להיות password (כוכביות)
    assert password_input.get_attribute("type") == "password", "❌ שדה הסיסמה לא התחיל כסוג חסוי (Password)"

    # 3. הקשחת CSS Selector: וידוא הזחת ה-Padding המוגן ל-48px קשיחים כפי שנקבע ב-style.css
    padding_left = password_input.value_of_css_property("padding-left")
    assert padding_left == "48px", f"❌ הגנת ה-CSS נפרצה! ה-Padding השמאלי הוא {padding_left} במקום 48px קשיחים"

    # 4. לחיצה על כפתור העין ווידוא שינוי הטיפוס לטקסט גלוי (👁️ -> 🙈)
    toggle_eye_btn.click()
    assert password_input.get_attribute("type") == "text", "❌ סוג השדה לא השתנה לטקסט גלוי לאחר לחיצה על כפתור העין"
    assert toggle_eye_btn.text == "🙈", "❌ אייקון העין לא השתנה ל-🙈 במצב גלוי"


@pytest.mark.ui
@pytest.mark.edge
@pytest.mark.xray("QA-104")
def test_admin_login_submit_via_enter_key(driver):
    """
    🧪 תרחיש קצה פונקציונלי: אימות שליחת טופס האבטחה באמצעות מקש ה-Enter במקלדת.
    מוודא נוחות משתמש (UX) וחסינות מנגנוני ה-Keydown ב-JavaScript.
    """
    wait = WebDriverWait(driver, 10)

    # 1. פתיחת המודאל והזנת סיסמה תקינה
    driver.find_element(By.ID, "adminToggleBtn").click()
    password_input = wait.until(ec.element_to_be_clickable((By.ID, "adminPassword")))
    password_input.send_keys("admin123")

    # 2. שליחת מקש ה-Enter אל תוך השדה במקום לחיצה פיזית על כפתור האימות
    password_input.send_keys(Keys.ENTER)

    # 3. וידוא פתיחת הלוח בהצלחה
    cms_panel = wait.until(ec.visibility_of_element_located((By.ID, "cmsPanel")))
    assert cms_panel.is_displayed(), "❌ לוח ה-CMS לא נפתח בעת שימוש במקש ה-Enter"
