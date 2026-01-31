from django.db import models
from django.conf import settings


class Like(models.Model):
    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "likes"
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="uk_likes_post_user")
        ]
