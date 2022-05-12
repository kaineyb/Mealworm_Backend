import os

from .common import *

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = []  # will update once we pick a platform
