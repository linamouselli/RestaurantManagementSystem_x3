from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Category name cannot be empty.")
        if Category.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError("Category with this name already exists.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}-{self.category.name}"

    def clean(self):
        errors = {}
        if not self.name.strip():
            errors['name'] = "Product name cannot be empty."
        if self.price <= 0:
            errors['price'] = "Product price must be greater than zero."
        if self.preparation_time < 1:
            errors['preparation_time'] = "Preparation time must be at least 1 minute."
        if self.category and not self.category.is_active:
            errors['category'] = "Cannot assign product to an inactive category."
        if Product.objects.exclude(pk=self.pk).filter(name__iexact=self.name, category=self.category).exists():
            errors['name'] = "Product with this name already exists in this category."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


