import os

from .common import *

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = [
    "food-shopper-api.herokuapp.com"
]  # will update once we pick a platform
