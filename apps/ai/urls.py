from django.urls import path
from .views.tone_api import ToneConverterAPIView

urlpatterns = [
    path("tone-convert/", ToneConverterAPIView.as_view(), name="tone_convert"),
]
