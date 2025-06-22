from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')  # ✅ Best way to load config.py

    db.init_app(app)
    mail.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
