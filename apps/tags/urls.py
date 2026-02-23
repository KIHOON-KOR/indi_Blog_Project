from django.urls import path
from apps.tags.views.tag_api import TagListAPIView

urlpatterns = [
    path("", TagListAPIView.as_view(), name="tag_list_stat"),
]
