from rest_framework import serializers
from .models import HealthIndicator


class HealthIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIndicator
        fields = '__all__'


class CustomHealthIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIndicator
        fields = ('name', )

    def save(self, **kwargs):
        return super(CustomHealthIndicatorSerializer, self).save(
            is_cuantitative=False,
            is_decimal=False,
            added_by=self.context['request'].user,
            min=1,
            max=10,
            **kwargs)
