from django.urls import path

from apps.comment.views.comment_api import CommentAPIView

urlpatterns = [
    path("<int:post_id>/", CommentAPIView.as_view(), name="comment_create"),
]
