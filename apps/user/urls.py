from django.urls import path

from apps.user.views.login import LoginAPIView


urlpatterns = [
    path("login", LoginAPIView.as_view(), name="login"),
]
