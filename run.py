# run.py

import os
from flask import Flask
from app.routes.dashboard import dashboard_bp
from app.routes.admin import admin_bp


def create_app() -> Flask:
    """מפעל אתחול האפליקציה (Application Factory) לפי ארכיטקטורת השכבות"""
    flask_app = Flask(
        __name__,
        template_folder=os.path.join('app', 'templates'),
        static_folder=os.path.join('app', 'static')
    )

    flask_app.secret_key = 'snir_portfolio_secret_key'

    # 🛡️ בידוד שכבות הרמטי: הגדרת קידומת ניתוב קשיחה ל-Blueprint של ה-API והדאשבורד
    flask_app.register_blueprint(dashboard_bp, url_prefix='/')
    flask_app.register_blueprint(admin_bp)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    # הרצת השרת בפורט 5000
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=5000, threaded=True)
