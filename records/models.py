from django.db import models
from users.models import User
from indicators.models import HealthIndicator


class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    health_indicator = models.ForeignKey(HealthIndicator, on_delete=models.CASCADE, null=False, related_name="records")
    date = models.DateTimeField(null=False)
    value = models.FloatField(null=False)
    alt_value = models.FloatField(null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user} {self.health_indicator} {self.date}"
