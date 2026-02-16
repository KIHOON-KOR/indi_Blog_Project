from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.core.models import TimeStampedModel
from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    nickname = models.CharField(
        max_length=50,
    )

    profile_img = models.CharField(max_length=255, null=True, blank=True)

    bio = models.CharField(max_length=150, null=True, blank=True) # 간단 자기소개

    # 활성화 여부: True면 로그인 가능, False면 계정 정지 등의 상태(기본값은 True)
    is_active = models.BooleanField(default=True)
    # 관리자 사이트 접속 권한 여부: True면 admin 페이지 접속 가능
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # 로그인 시 식별자로 사용할 필드를 지정합니다. 여기서는 'email'을 아이디로 씁니다.
    USERNAME_FIELD = "email"  # 로그인은 이메일로
    # createsuperuser 커맨드로 관리자 계정을 만들 때, 이메일/비번 외에 추가로 입력받을 필드입니다.
    REQUIRED_FIELDS = ["nickname"]  # createsuperuser 할 때 물어볼 필드

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self) -> str:
        return f"{self.nickname} ({self.email})"
