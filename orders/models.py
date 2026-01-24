from django.db import models
from products.models import Product 
from customers.models import Customer
from django.core.exceptions import ValidationError

class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.first_name}"

    def can_change_status(self, new_status):
        order_flow = ['New', 'Preparing', 'Ready', 'Delivered']
        current_index = order_flow.index(self.status)
        try:
            new_index = order_flow.index(new_status)
        except ValueError:
            raise ValidationError(f"Invalid status: {new_status}")

        if new_index != current_index + 1:
            raise ValidationError(f"Status must progress step by step: {self.status} → {new_status}")
        return True

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
