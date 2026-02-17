from django.urls import path

from apps.core.page_views import home

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
]
