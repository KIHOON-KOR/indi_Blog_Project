from django.urls import path

from apps.post.views.page_views import post_write_page
from apps.post.views.post_api import PostAPIView


urlpatterns = [
    path("", PostAPIView.as_view(), name="post_create"),
    path("write/", post_write_page, name="post_write_page")
]
