from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)

email_validator = EmailValidator( message="Enter a valid email address.")


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[email_validator]
    )
    phone = models.CharField(
        max_length=10,
        validators=[phone_validator]
    )
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if len(self.first_name) < 2:
            raise ValidationError("First name must be at least 2 characters long.")

        if len(self.last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters long.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


