from django.db import models
from users.models import User


class HealthIndicator(models.Model):
    name = models.CharField(max_length=64, null=False)
    medical_name = models.CharField(max_length=64, blank=True, null=True)
    is_cuantitative = models.BooleanField(null=False)
    is_decimal = models.BooleanField(null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unit_of_measurement = models.CharField(max_length=16, blank=True, null=True)
    min = models.FloatField(null=False)
    max = models.FloatField(null=False)

    def __str__(self) -> str:
        # noinspection PyTypeChecker
        return self.name

    @property
    def is_custom(self) -> bool:
        return self.added_by is not None

    @property
    def medical_name_(self) -> str:
        # noinspection PyTypeChecker
        return self.medical_name if self.medical_name else self.name
