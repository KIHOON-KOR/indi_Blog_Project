from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.series.models import Series
from apps.tags.models.tag import Tag


class Post(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    series = models.ForeignKey(
        Series, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    series_order = models.BigIntegerField(null=True, blank=True)

    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)

    is_temp = models.BooleanField(default=False)

    # Soft Delete 필드
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Tag와의 M:N 관계 (Through 설정)
    tags = models.ManyToManyField(Tag, through="tags.PostTag", related_name="posts")

    class Meta:
        db_table = "posts"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title
