from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.post.models.post import Post

class Comment(TimeStampedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()

    class Meta:
        db_table = "comments"