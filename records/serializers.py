from rest_framework import serializers
from .models import HealthRecord


class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = "__all__"


class HealthRecordInputSerializer(serializers.Serializer):
    health_indicator_id = serializers.IntegerField(required=True)
    value = serializers.FloatField(required=True)
    note = serializers.CharField(required=False, allow_blank=True)
