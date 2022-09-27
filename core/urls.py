from django.urls import path
from django.views.generic import TemplateView

import core.views

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html")),
    path("current-key/", core.views.current_key, name="results"),
]
