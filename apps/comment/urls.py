from django.urls import path

from apps.comment.views.comment_api import CommentAPIView
from apps.comment.views.comment_manage_api import CommentManageAPIView

urlpatterns = [
    path("<int:post_id>/", CommentAPIView.as_view(), name="comment_create"),
    path(
        "post/<int:comment_id>/", CommentManageAPIView.as_view(), name="comment_update"
    ),
]
