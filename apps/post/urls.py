from django.urls import path

from apps.post.views.post_api import PostAPIView


urlpatterns = [
    path("", PostAPIView.as_view(), name="post_create"),
]
