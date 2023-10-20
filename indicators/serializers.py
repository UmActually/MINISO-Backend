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
