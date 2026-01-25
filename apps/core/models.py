from django.db import models


class TimeStampedModel(models.Model):
    """
    모든 모델의 기본이 되는 추상 모델
    생성일(created_at)과 수정일(updated_at)을 자동으로 관리합니다.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
