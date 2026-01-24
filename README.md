# Restaurant Management System API

## 📌 Description
This Django REST API Final Project is designed for a simple restaurant management system.
It allows managing **customers, products, categories, orders, and users**.
The API supports role-based permissions, Simple JWT authentication, pagination, and filtering.

---

## 🧱 Application Structure
RestaurantManagementSystem_x/
├── customers/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tests.py
│   └── urls.py
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tests.py
│   └── urls.py
│   └── admin.py

├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
│   └── urls.py
│   └── admin.py


├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── permissions.py
│   └── tests.py
│   └── urls.py
│   └── admin.py



├── restaurant/
│   └── asgi.py
│   └── settings.py
│   └── urls.py
│   └── wsgi.py

├── manage.py
├── requirements.txt
└── README.md

---

## 📊 Models Overview

### Customer Model
| Field | Type | Description |
|-------|------|------------|
| first_name | CharField | Customer first name |
| last_name | CharField | Customer last name |
| email | EmailField | Unique email |
| phone | CharField | Phone number |
| address | TextField | Address |
| registration_date | DateTimeField | Auto generated |

### Product Model
| Field | Type | Description |
|-------|------|------------|
| name | CharField | Product name |
| description | TextField | Description |
| price | DecimalField | Price |
| category | ForeignKey | Category of product |
| is_available | BooleanField | Availability |
| preparation_time | PositiveIntegerField | Time to prepare |

### Category Model
| Field | Type | Description |
|-------|------|------------|
| name | CharField | Category name |
| description | TextField | Description |
| is_active | BooleanField | Active status |

### Order Model
| Field | Type | Description |
|-------|------|------------|
| customer | ForeignKey | Customer placing the order |
| order_date | DateTimeField | Auto-generated order date |
| total_amount | DecimalField | Total price of order |
| status | CharField | New, Preparing, Ready, Delivered |
| notes | TextField | Optional notes |

### OrderItem Model
| Field | Type | Description |
|-------|------|------------|
| order | ForeignKey | Associated order |
| product | ForeignKey | Product ordered |
| quantity | PositiveIntegerField | Quantity |
| price_at_order | DecimalField | Product price at order |

### CustomUser Model
| Field | Type | Description |
|-------|------|------------|
| username | CharField | User username |
| email | EmailField | User email |
| password | CharField | User password (hashed) |
| role | CharField | Role: admin, manager, staff |

---

## 🔁 API Endpoints

### Customers
| Method | Endpoint | Description |
|--------|---------|------------|
| GET | /customers/ | List all customers |
| POST | /customers/ | Create new customer |
| GET | /customers/{id}/ | Retrieve customer details |
| PUT | /customers/{id}/ | Update customer |
| DELETE | /customers/{id}/ | Delete customer |
PATCH NOT INCLUDED
**Permissions**: Admin=CRUD, Manager=Read only, Staff=None

### Products
| Method | Endpoint | Description |
|--------|---------|------------|
| GET | /products/ | List all products |
| POST | /products/ | Add new product |
| GET | /products/{id}/ | Get product by ID |
| PUT | /products/{id}/ | Update product |
| DELETE | /products/{id}/ | Delete product |
| GET | /products/available/ | List available products |
PATCH NOT INCLUDED
**Permissions**: Admin=CRUD, Manager=CRUD, Staff=Read only for list/retrieve

### Categories
| Method | Endpoint | Description |
|--------|---------|------------|
| GET | /categories/ | List all categories |
| POST | /categories/ | Add new category |
| GET | /categories/{id}/ | Get category details |
| PUT | /categories/{id}/ | Update category |
| DELETE | /categories/{id}/ | Delete category |
PATCH NOT INCLUDED
**Permissions**: Admin=CRUD, Manager=CRUD, Staff=None for modification

### Orders
| Method | Endpoint | Description |
|--------|---------|------------|
| GET | /orders/ | List all orders |
| POST | /orders/ | Create new order |
| GET | /orders/{id}/ | Retrieve order details |
| PUT | /orders/{id}/status/ | Update order status |
PATCH & DELETE NOT INCLUDED
**Permissions**: Admin=CRUD, Manager=CRUD, Staff=Create/View only

### Users
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | /users/login/ | Login and receive JWT |
| GET | /users/profile/ | Retrieve own profile |
**Permissions**: profile requires authentication

---

## 🔐 Authentication
- Simple JWT Authentication implemented via **djangorestframework-simplejwt**
- Protected endpoints require Authorization header:
Authorization: Bearer <access_token>

---

## 📑 Pagination
-  5 items per page  
- Implemented using `PageNumberPagination` in DRF

---

## 🔍 Filtering & Search
- Products: filter by `category__name`, `price`  
- Orders: filter by `customer`, `status`  
- Products: search by `name`
- ---

## ⚙️ Installation
```bash
git clone https://github.com/linamouselli/RestaurantManagementSystem_x3.git
cd RestaurantManagementSystem_x3
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
Django
djangorestframework
djangorestframework-simplejwt
django-filter
drf-spectacular

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Notes & Business Rules:

Cannot order unavailable products
Order total is calculated automatically
Order statuses: New → Preparing → Ready → Delivered
Product availability is updated when ordered
Admin can manage everything
Manager can manage products/categories and view orders/customers
Staff can only create/view orders and view products/categories

## Category API Tests
1- Anyone can list categories
2- Admin can create categories
3- Staff cannot create category

## Product API Tests

1- Anyone can list products
2- Invalid price rejected
3- Inactive category rejected
4- Admin can create valid product
5- Available products endpoint returns only available
6- Staff cannot create product

## Customer API Tests

1-Admin can create customer
2-Manager can view customers
3-Staff cannot access customers
4-Invalid phone rejected
5-First name min length rejected

## Order API Tests

1- Staff can create order
2- Cannot order unavailable product
3- Authenticated user can list orders
4- Admin can update order status step by step
5- Admin cannot skip status steps (e.g., New → Ready) 
6- Invalid status rejected
7- Staff cannot update order status


python manage.py test
python manage.py test products 
python manage.py test customers 
python manage.py test orders
