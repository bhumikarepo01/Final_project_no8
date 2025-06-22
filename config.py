import os

SECRET_KEY = 'mysecretkey'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", "sqlite:///database.db"
)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'bhumikajayswal01@gmail.com'   # We’ll update later
MAIL_PASSWORD = 'ypywnqquyuuilnwo'   # We’ll update later
