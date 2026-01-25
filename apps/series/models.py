from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Series(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="series"
    )
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "series"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="uk_series_user_name"
            )
        ]

    def __str__(self):
        return self.name