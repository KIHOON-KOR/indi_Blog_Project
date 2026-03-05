from django.urls import path
from apps.tags.views.tag_api import TagListAPIView, MyTagListAPIView

urlpatterns = [
    path("", TagListAPIView.as_view(), name="tag_list_stat"),
    path("my/", MyTagListAPIView.as_view(), name="my_tag_list_stat"),
]
