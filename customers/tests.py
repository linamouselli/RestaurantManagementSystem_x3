
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from customers.models import Customer
from django.urls import reverse


User = get_user_model()


class CustomerAPITest(APITestCase):

    def setUp(self):
        # Users
        self.admin = User.objects.create_user(
            username='admin',
            password='admin12345',
            role='admin'
        )

        self.manager = User.objects.create_user(
            username='manager',
            password='manager12345',
            role='manager'
        )

        self.staff = User.objects.create_user(
            username='staff',
            password='staff12345',
            role='staff'
        )

        self.customer_data = {
            "first_name": "Sara",
            "last_name": "Ali",
            "email": "sara@test.com",
            "phone": "0999999999",
            "address": "Damascus"
        }

        self.url = "/api/customers/"

    def test_admin_can_create_customer(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, self.customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)


    def test_manager_can_view_customers(self):
        Customer.objects.create(**self.customer_data)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_cannot_access_customers(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_invalid_phone_validation(self):
        self.client.force_authenticate(user=self.admin)

        invalid_data = self.customer_data.copy()
        invalid_data["phone"] = "123"

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_first_name_min_length_validation(self):
        self.client.force_authenticate(user=self.admin)
        invalid_data = self.customer_data.copy()
        invalid_data["first_name"] = "A"
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

