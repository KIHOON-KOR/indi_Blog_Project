from django.urls import path

from apps.post.views.page_views import (
    post_write_page,
    temp_post_list_page,
    my_post_list_page,
    global_post_list_page,
)

from apps.post.views.post_api import PostAPIView, MyPostAPIView
from apps.post.views.temp_post_api import MyTempManageAPIView, MyTempAPIView

urlpatterns = [
    # [전체 피드 및 생성]
    path("", PostAPIView.as_view(), name="post_list_create"),

    # [내 블로그]
    path("my/", MyPostAPIView.as_view(), name="post_my_list"),

    # [임시글 관리]
    path("my/temp/", MyTempAPIView.as_view(), name="post_temp_list"),
    path(
        "my/temp/<int:post_id>/", MyTempManageAPIView.as_view(), name="post_temp_manage"
    ),

    # [화면(UI)]
    path("write/", post_write_page, name="post_write_page"),
    path("my/page/", my_post_list_page, name="my_post_list_page"),
    path("all/page/", global_post_list_page, name="global_post_list_page"),
    path("my/temp/page/", temp_post_list_page, name="temp_post_list_page"),
]
