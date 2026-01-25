from django.db import models
from django.conf import settings 

class SocialAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="social_accounts"
    )
    
    provider = models.CharField(max_length=20)
    social_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "social_accounts"
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "social_id"], 
                name="uk_social_provider_id"
            )
        ]