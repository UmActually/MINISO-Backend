from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserRole(models.IntegerChoices):
    PATIENT = 0, "Patient"
    DOCTOR = 1, "Doctor"
    ADMIN = 2, "Admin"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["is_superuser"] = True
        extra_fields["is_staff"] = True
        extra_fields["role"] = UserRole.ADMIN

        extra_fields.setdefault("first_names", "Alan")
        extra_fields.setdefault("last_names", "Turing")
        extra_fields.setdefault("birth_date", "1912-06-23")
        extra_fields.setdefault("height", 1.78)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, null=False)
    role = models.SmallIntegerField(choices=UserRole.choices, default=UserRole.PATIENT, null=False)

    first_names = models.CharField(max_length=64, null=False)
    last_names = models.CharField(max_length=64, null=False)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=False)
    birth_date = models.DateField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

    doctor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True,
        related_name="patients", default=None)

    is_staff = models.BooleanField(default=False, null=False)
    password_reset_token = models.CharField(max_length=128, null=True)

    objects = UserManager()

    def __str__(self):
        return self.email
