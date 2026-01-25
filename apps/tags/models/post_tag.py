from django.db import models

from apps.post.models.post import Post
from apps.tags.models.tag import Tag

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    

    class Meta:
        db_table = "post_tags"
        constraints = [
            models.UniqueConstraint(
                fields=["post", "tag"],
                name="uk_post_tags_composite"
            )
        ]