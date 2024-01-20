import os

from django.shortcuts import render


def current_key(request):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        return None

    key = SECRET_KEY[:5]
    return render(request, "core/current_key.html", {"key": key})
