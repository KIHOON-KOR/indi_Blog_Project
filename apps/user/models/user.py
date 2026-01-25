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

    bio = models.CharField(max_length=150, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"  # 로그인은 이메일로
    REQUIRED_FIELDS = ["nickname"]  # createsuperuser 할 때 물어볼 필드

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self) -> str:
        return f"{self.nickname} ({self.email})"
