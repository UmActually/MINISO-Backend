from django.db import models
from users.models import User
from indicators.models import HealthIndicator


class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    health_indicator = models.ForeignKey(HealthIndicator, on_delete=models.CASCADE, null=False)
    date = models.DateField(null=False)
    value = models.FloatField(null=False)
    note = models.TextField(null=True)
