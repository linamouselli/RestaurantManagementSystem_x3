from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Customer
from .serializers import CustomerSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all customers",
        description="Retrieve a list of all customers in our restaurant.",
        responses={200: CustomerSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get customer details",
        description="Retrieve details of a specific customer by ID.",
    ),
    create=extend_schema(
        summary="Create a new customer",
        description="Add a new customer to our restaurant.",
    ),
    update=extend_schema(
        summary="Update a customer",
        description="Update all fields of a specific customer.",
    ),
    destroy=extend_schema(
        summary="Delete a customer",
        description="Remove a customer from the restaurant.",
    ),
)
class CustomerViewSet(ModelViewSet):
    """
    Customer Management API

    This ViewSet provides full CRUD operations for Customers.

    Available operations:
    - list: Retrieve all customers
    - retrieve: Retrieve a specific customer by ID
    - create: Add a new customer
    - update: Update an existing customer
    - delete: Delete a customer

    Authentication:
    - Requires JWT Authentication
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


