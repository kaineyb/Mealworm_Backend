import os

import dj_database_url

from .common import *

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = [
    "food-shopper-api.herokuapp.com"
]  # will update once we pick a platform


CORS_ALLOWED_ORIGINS = [
    "https://food-shopper-kjb.herokuapp.com",
]


DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)
