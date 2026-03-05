from django.urls import path

from apps.post.views.page_views import (
    post_write_page,
    temp_post_list_page,
    my_post_list_page,
    global_post_list_page,
    post_detail_page,
    post_edit_page,
)

from apps.post.views.post_api import PostAPIView, MyPostAPIView, PostDetailAPIView
from apps.post.views.post_like_api import PostLikeAPIView
from apps.post.views.temp_post_api import MyTempManageAPIView, MyTempAPIView
from apps.post.views.trash.trash_api import TrashAPIView, TrashManageAPIView

urlpatterns = [
    # [전체 피드 및 생성]
    path("", PostAPIView.as_view(), name="post_list_create"),
    # [내 블로그]
    path("my/", MyPostAPIView.as_view(), name="post_my_list"),
    path("<int:post_id>/", PostDetailAPIView.as_view(), name="post_detail_manage"),
    # [임시글 관리]
    path("my/temp/", MyTempAPIView.as_view(), name="post_temp_list"),
    path(
        "my/temp/<int:post_id>/", MyTempManageAPIView.as_view(), name="post_temp_manage"
    ),
    # [좋아요 등록/취소]
    path("<int:post_id>/likes/", PostLikeAPIView.as_view(), name="post_like"),

    # [휴지통 관리]
    path("my/trash/", TrashAPIView.as_view(), name="post_trash_list"),
    path("my/trash/<int:post_id>/", TrashManageAPIView.as_view(), name="post_trash_detail"),

    # [화면(UI)]
    path("write/", post_write_page, name="post_write_page"),
    path("my/page/", my_post_list_page, name="my_post_list_page"),
    path("all/page/", global_post_list_page, name="global_post_list_page"),
    path("my/temp/page/", temp_post_list_page, name="temp_post_list_page"),
    path("<int:post_id>/page/", post_detail_page, name="post_detail_page"),
    path("<int:post_id>/edit/page/", post_edit_page, name="post_edit_page"),
]
