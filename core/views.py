from django.shortcuts import render
from food_shopper.settings.prod import SECRET_KEY


def current_key(request):
    key = SECRET_KEY[:5]
    return render(request, "core/current_key.html", {"key": key})
