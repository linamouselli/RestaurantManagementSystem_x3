from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")

        extra_fields.setdefault('role', 'staff')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('role') != 'admin':
            raise ValueError("Superuser must have role='admin'")

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username
