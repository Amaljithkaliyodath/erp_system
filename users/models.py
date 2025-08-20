# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom manager to handle user creation.
    Ensures that superusers are always Admin role.
    """

    def create_user(self, username, email=None, password=None, role="Employee", **extra_fields):
        if not username:
            raise ValueError("The Username must be set")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Force role = Admin when creating a superuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username=username,
            email=email,
            password=password,
            role="Admin",   # ✅ Force Admin
            **extra_fields
        )


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Manager", "Manager"),
        ("Employee", "Employee"),
    ]

    # ✅ Only letters allowed in username
    username_validator = RegexValidator(
        regex=r"^[A-Za-z]+$",
        message="Username must contain only letters (A-Z, a-z)."
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={"unique": "A user with this username already exists."},
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="Employee"
    )

    objects = CustomUserManager()  # ✅ Attach custom manager

    def __str__(self):
        return f"{self.username} ({self.role})"
