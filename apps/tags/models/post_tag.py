from django.db import models


class PostTag(models.Model):
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE)
    tag = models.ForeignKey("tags.Tag", on_delete=models.CASCADE)

    class Meta:
        db_table = "post_tags"
        constraints = [
            models.UniqueConstraint(
                fields=["post", "tag"], name="uk_post_tags_composite"
            )
        ]
