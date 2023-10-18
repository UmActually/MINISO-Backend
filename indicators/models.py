from django.db import models
from users.models import User


class HealthIndicator(models.Model):
    name = models.CharField(max_length=64, null=False)
    is_cuantitative = models.BooleanField(null=False)
    is_decimal = models.BooleanField(null=False)
    is_custom = models.BooleanField(null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unit_of_measurement = models.CharField(max_length=64, null=False)
    min = models.FloatField(null=False)
    max = models.FloatField(null=False)
