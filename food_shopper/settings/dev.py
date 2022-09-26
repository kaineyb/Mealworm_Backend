from .common import *

DEBUG = True
SECRET_KEY = "XYZ"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "NAME": os.environ["DATABASE_NAME"],
        "ENGINE": "django.db.backends.mysql",
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASS"],
        # "OPTIONS": {
        #     "autocommit": True,
        # },
    }
}
