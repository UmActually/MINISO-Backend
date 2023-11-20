from rest_framework import serializers
from .models import HealthIndicator


class HealthIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIndicator
        fields = '__all__'


class HealthIndicatorDeserializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, required=True)
    medical_name = serializers.CharField(max_length=64, required=False)
    is_cuantitative = serializers.BooleanField(required=True)
    is_decimal = serializers.BooleanField(required=False)
    min = serializers.FloatField(required=False)
    max = serializers.FloatField(required=False)
    unit_of_measurement = serializers.CharField(max_length=16, required=False)

    def validate(self, attrs):
        if attrs['is_cuantitative']:
            if any(field not in attrs for field in ('is_decimal', 'min', 'max')):
                raise serializers.ValidationError(
                    f"is_decimal, min, and max are required when indicator is cuantitative")
            if attrs['min'] > attrs['max']:
                raise serializers.ValidationError("min must be less than max (come on, you're better than this)")
        else:
            attrs['is_decimal'] = False
            attrs.setdefault('min', 1)
            attrs.setdefault('max', 10)
            attrs['unit_of_measurement'] = None
        return attrs

    def create(self, validated_data):
        return HealthIndicator.objects.create(**validated_data)


class CustomHealthIndicatorDeserializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, required=True)

    def create(self, validated_data):
        return HealthIndicator.objects.create(
            is_cuantitative=False,
            is_decimal=False,
            added_by=self.context['request'].user,
            min=1,
            max=10,
            **validated_data
        )
