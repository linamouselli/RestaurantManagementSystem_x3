from rest_framework.test import APITestCase
from django.urls import reverse
from products.models import Category, Product
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTestCase(APITestCase):
    def setUp(self):
        # Users
        self.admin = CustomUser.objects.create_user(username='admin', password='admin123', role='admin')
        self.manager = CustomUser.objects.create_user(username='manager', password='manager123', role='manager')
        self.staff = CustomUser.objects.create_user(username='staff', password='staff123', role='staff')

        # JWT Tokens
        self.admin_token = str(RefreshToken.for_user(self.admin).access_token)
        self.manager_token = str(RefreshToken.for_user(self.manager).access_token)
        self.staff_token = str(RefreshToken.for_user(self.staff).access_token)

        # Categories
        self.cat1 = Category.objects.create(name="Appetizers", description="Starter dishes")
        self.cat2 = Category.objects.create(name="Main Course", description="Main dishes")

        # Products
        self.prod1 = Product.objects.create(
            name="Burger", description="Tasty burger", price=10.5, category=self.cat2, preparation_time=15
        )
        self.prod2 = Product.objects.create(
            name="Salad", description="Fresh salad", price=5, category=self.cat1, preparation_time=5
        )


class CategoryTests(BaseTestCase):

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
        else:
            self.assertEqual(len(response.data), 2)

    def test_create_category_admin(self):
        url = reverse('category-list')
        data = {"name": "Desserts", "description": "Sweet dishes"}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 3)

    def test_create_category_staff_forbidden(self):
        url = reverse('category-list')
        data = {"name": "Desserts", "description": "Sweet dishes"}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.staff_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)


class ProductTests(BaseTestCase):

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
        else:
            self.assertEqual(len(response.data), 2)

    def test_create_product_invalid_price(self):
        url = reverse('product-list')
        data = {
            "name": "Pizza",
            "description": "Cheese Pizza",
            "price": -5,
            "category_id": self.cat2.id,
            "is_available": True,
            "preparation_time": 10
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('price', response.data)

    def test_create_product_invalid_category(self):
        self.cat2.is_active = False
        self.cat2.save()
        url = reverse('product-list')
        data = {
            "name": "Pizza",
            "description": "Cheese Pizza",
            "price": 12,
            "category_id": self.cat2.id,
            "is_available": True,
            "preparation_time": 10
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('category', response.data)

    def test_create_product_valid(self):
        url = reverse('product-list')
        data = {
            "name": "Pizza",
            "description": "Cheese Pizza",
            "price": 12.5,
            "category_id": self.cat2.id,
            "is_available": True,
            "preparation_time": 10
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 3)

    def test_available_products_endpoint(self):
        url = reverse('product-available-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
        else:
            self.assertEqual(len(response.data), 2)

        self.prod1.is_available = False
        self.prod1.save()
        response = self.client.get(url)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_product_creation_by_staff_forbidden(self):
        url = reverse('product-list')
        data = {
            "name": "Soup",
            "description": "Hot soup",
            "price": 6,
            "category_id": self.cat1.id,
            "is_available": True,
            "preparation_time": 8
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.staff_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
