from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "email", "role", "first_names", "last_names",
            "phone_number", "date_joined", "birth_date",
            "height", "medical_history", "doctor")
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "role": {"read_only": True},
        }

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()
        user = self.instance

        if user.role != UserRole.PATIENT:
            fields.pop("birth_date")
            fields.pop("height")
            fields.pop("medical_history")
            fields.pop("doctor")

        return fields


class PatientDeserializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_names = serializers.CharField(max_length=64, required=True)
    last_names = serializers.CharField(max_length=64, required=True)
    doctor_id = serializers.IntegerField(required=True)
    birth_date = serializers.DateField(required=True)
    height = serializers.FloatField(required=False)
    phone_number = serializers.CharField(max_length=16, required=False)
    medical_history = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use")

        doctor_id = attrs["doctor_id"]
        if not User.objects.filter(id=doctor_id, role=UserRole.DOCTOR).exists():
            raise serializers.ValidationError("The doctor user doesn't exist, or doesn't have the role of doctor")

        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class DoctorDeserializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_names = serializers.CharField(max_length=64, required=True)
    last_names = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=16, required=False)

    def validate(self, attrs):
        email = attrs["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use")
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(role=UserRole.DOCTOR, **validated_data)
