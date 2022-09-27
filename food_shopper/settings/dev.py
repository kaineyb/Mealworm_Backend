import secrets

from .common import *

DEBUG = True
SECRET_KEY = secrets.token_urlsafe(16)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
