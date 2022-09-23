import os

from .common import *

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = ["api.mealworm.uk"]  # will update once we pick a platform


CORS_ALLOWED_ORIGINS = [
    "https://mealworm.uk",
]


DATABASES = {
    "default": {
        "NAME": os.environ["DATABASE_NAME"],
        "ENGINE": "django.db.backends.mysql",
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASS"],
        "OPTIONS": {
            "autocommit": True,
        },
    }
}
