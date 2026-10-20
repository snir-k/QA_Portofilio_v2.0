# app/routes/admin.py

from flask import Blueprint, request, redirect, url_for, flash
from app.data.data_manager import db_manager
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/update-content', methods=['POST'])
def update_content_admin():
    welcome_text = request.form.get('welcome_text', '').strip()
    if welcome_text:
        db_manager.update_cms_settings({"welcome_text": welcome_text})
    return redirect(url_for('dashboard.display_dashboard'))


@admin_bp.route('/admin/add-tech', methods=['POST'])
def add_tech_admin():

    tech_name = request.form.get('tech_name', '').strip()
    tech_color = request.form.get('tech_color', '#FFFFFF').strip()

    # 📁 טיפול בהעלאת האייקון מהמחשב
    icon_file = request.files.get('tech_icon')
    icon_path = "/static/assets/default-icon.png"  # ברירת מחדל

    if icon_file and icon_file.filename != '':
        # הבטחת שם קובץ מאובטח ויצירת נתיב שמירה פיזי בתיקיית הסטטיק
        filename = secure_filename(f"{tech_name}_{icon_file.filename}")
        upload_folder = os.path.join('app', 'static', 'assets')

        # יצירת התיקייה פיזית במחשב אם היא עדיין לא קיימת
        os.makedirs(upload_folder, exist_ok=True)

        # שמירת הקובץ
        icon_file.save(os.path.join(upload_folder, filename))
        icon_path = f"/static/assets/{filename}"

    if tech_name:
        db_manager.add_technology(tech_name, icon_path, tech_color)
        flash(f"הטכנולוגיה {tech_name} והאייקון הועלו בהצלחה!", "success")

    return redirect(url_for('dashboard.display_dashboard'))

@admin_bp.route('/admin/delete-tech', methods=['POST'])
def delete_tech_admin():
    tech_name = request.form.get('tech_name', '').strip()
    if tech_name:
        db_manager.delete_technology(tech_name)
    return redirect(url_for('dashboard.display_dashboard'))
