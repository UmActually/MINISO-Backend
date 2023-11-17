import datetime
import pytz

from rest_framework import serializers

from indicators.models import HealthIndicator
from indicators.serializers import HealthIndicatorSerializer
from .models import HealthRecord


MEXICO_TIME_ZONE = pytz.timezone("Mexico/General")


class HealthRecordSerializer(serializers.ModelSerializer):
    health_indicator = HealthIndicatorSerializer()

    class Meta:
        model = HealthRecord
        fields = "__all__"


class HealthRecordMinimalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    value = serializers.FloatField()
    note = serializers.CharField()


def group_records_by_date(health_records):
    records_by_day = []
    current_day = 0
    for record in health_records:
        day = record.date.astimezone(MEXICO_TIME_ZONE).day
        if day != current_day:
            current_day = day
            records_by_day.append([record])
        else:
            records_by_day[-1].append(record)

    return [
        HealthRecordSerializer(records, many=True).data
        for records in records_by_day
    ]


# def to_representation(self, instance):
#     # Agrupar los registros por día
#     records_by_day = {}
#     for record in instance["health_records"]:
#         records_by_day.setdefault(record.date, []).append(record)
#
#     # Serializar cada grupo
#     return [
#         HealthRecordSerializer(records, many=True).data
#         for records in records_by_day.values()
#     ]


class HealthRecordDeserializer(serializers.Serializer):
    health_indicator_id = serializers.IntegerField(required=True)
    value = serializers.FloatField(required=True)
    note = serializers.CharField(required=False, allow_blank=True)

    # TODO: Esto es solo para pruebas, quitarlo después
    date = serializers.DateTimeField(required=False)

    def validate(self, attrs):
        # Validar que el indicador exista
        health_indicator_id = attrs["health_indicator_id"]
        try:
            health_indicator = HealthIndicator.objects.get(id=health_indicator_id)
        except HealthIndicator.DoesNotExist:
            raise serializers.ValidationError("This health indicator doesn't exist")

        # Validar que el usuario tenga permiso para agregar registros de este indicador
        if health_indicator.is_custom and health_indicator.added_by != self.context["request"].user:
            raise serializers.ValidationError("You can't add records to this indicator")

        # Validar que el valor esté dentro del rango
        value = attrs["value"]
        if not (health_indicator.min <= value <= health_indicator.max):
            raise serializers.ValidationError("Value out of range")

        return attrs

    def create(self, validated_data):
        date = validated_data.pop(
            "date",
            datetime.datetime.now().astimezone(MEXICO_TIME_ZONE))
        return HealthRecord.objects.create(
            user=self.context["request"].user,
            date=date,
            **validated_data
        )
