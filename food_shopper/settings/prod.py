import os
import secrets

import dj_database_url

from .common import *

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(16)

ALLOWED_HOSTS = [
    "api.mealworm.uk",
    ".onrender.com",
]

CORS_ALLOWED_ORIGINS = [
    "https://mealworm.uk",
]

# Allow Render preview URLs in CORS
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.onrender\.com$",
]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}
