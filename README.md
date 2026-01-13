# Customer Management API

## 📌 Description
This Django REST API is used to manage customers data.
It provides CRUD operations for customer management and is designed
to be extended with JWT authentication.

---

## 🧱 Application Structure
customers/
├── models.py
├── serializers.py
├── views.py
├── urls.py

---

## 📊 Customer Model
| Field | Type | Description |
|------|------|------------|
| first_name | CharField | Customer first name |
| last_name | CharField | Customer last name |
| email | EmailField | Unique email |
| phone | CharField | Phone number |
| address | TextField | Address |
| registration_date | DateTimeField | Auto generated |

---

## 🔁 API Endpoints
| Method | Endpoint | Description |
|------|--------|------------|
| GET | /customers/ | Get all customers |
| POST | /customers/ | Create new customer |
| GET | /customers/{id}/ | Get customer by ID |
| PUT | /customers/{id}/ | Update customer |
| DELETE | /customers/{id}/ | Delete customer |

---

## 🔐 Authentication
Currently, the API is open.
JWT authentication can be added to secure endpoints.

---

## ⚙️ Installation
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
