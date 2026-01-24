from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from customers.models import Customer
from products.models import Category, Product
from orders.models import Order, OrderItem

User = get_user_model()


class OrderAPITest(APITestCase):

    def setUp(self):
        # Users
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            role='admin'
        )

        self.staff = User.objects.create_user(
            username='staff',
            password='staff123',
            role='staff'
        )

        # Customer
        self.customer = Customer.objects.create(
            first_name="Sara",
            last_name="Ali",
            email="sara@test.com",
            phone="0999999999",
            address="Damascus"
        )

        # Category
        self.category = Category.objects.create(
            name="Pizza",
            description="Pizza category"
        )

        # Products
        self.product1 = Product.objects.create(
            name="Margherita",
            description="Cheese pizza",
            price=10,
            category=self.category,
            is_available=True,
            preparation_time=15
        )

        self.product2 = Product.objects.create(
            name="Pepperoni",
            description="Pepperoni pizza",
            price=15,
            category=self.category,
            is_available=True,
            preparation_time=20
        )

        self.unavailable_product = Product.objects.create(
            name="Unavailable",
            description="No stock",
            price=8,
            category=self.category,
            is_available=False,
            preparation_time=10
        )

        self.orders_url = "/api/orders/"

    def test_create_order_success(self):
        self.client.force_authenticate(user=self.staff)

        payload = {
            "customer": self.customer.id,
            "items": [
                {"product": self.product1.id, "quantity": 2},
                {"product": self.product2.id, "quantity": 1},
            ],
            "notes": "Extra cheese"
        }

        response = self.client.post(self.orders_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.total_amount, 35)  # (10*2) + (15*1)

    def test_cannot_order_unavailable_product(self):
        self.client.force_authenticate(user=self.staff)

        payload = {
            "customer": self.customer.id,
            "items": [
                {"product": self.unavailable_product.id, "quantity": 1},
            ]
        }

        response = self.client.post(self.orders_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_authenticated(self):
        Order.objects.create(customer=self.customer)

        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_order_status(self):
        order = Order.objects.create(customer=self.customer)

        self.client.force_authenticate(user=self.admin)
        url = f"/api/orders/{order.id}/status/"

        response = self.client.put(
            url,
            {"status": "Preparing"},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "Preparing")

    def test_invalid_status_rejected(self):
        order = Order.objects.create(customer=self.customer)

        self.client.force_authenticate(user=self.admin)
        url = f"/api/orders/{order.id}/status/"

        response = self.client.put(
            url,
            {"status": "Canceled"},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_cannot_update_order_status(self):
        order = Order.objects.create(customer=self.customer)

        self.client.force_authenticate(user=self.staff)
        url = f"/api/orders/{order.id}/status/"

        response = self.client.put(
            url,
            {"status": "Ready"},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_progress_status_step_by_step(self):
        self.client.force_authenticate(user=self.admin)
        order = Order.objects.create(customer=self.customer)
        url = f"/api/orders/{order.id}/status/"

        steps = ['New', 'Preparing', 'Ready', 'Delivered']

        for i in range(1, len(steps)):
            response = self.client.put(url, {"status": steps[i]}, format='json')
            self.assertEqual(response.status_code, 200)
            order.refresh_from_db()
            self.assertEqual(order.status, steps[i])

    def test_cannot_skip_status_step(self):
        self.client.force_authenticate(user=self.admin)
        order = Order.objects.create(customer=self.customer)
        url = f"/api/orders/{order.id}/status/"

        # Attempt to skip from 'New' → 'Ready'
        response = self.client.put(url, {"status": "Ready"}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("progress step by step", str(response.data))
