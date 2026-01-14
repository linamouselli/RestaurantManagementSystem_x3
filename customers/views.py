from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Customer
from .serializers import CustomerSerializer


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

    @swagger_auto_schema(
        operation_summary="Get all customers",
        operation_description="Retrieve a list of all registered customers.",
        responses={200: CustomerSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create new customer",
        operation_description="Create a new customer with personal information.",
        request_body=CustomerSerializer,
        responses={201: CustomerSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get customer by ID",
        operation_description="Retrieve details of a specific customer using ID.",
        responses={200: CustomerSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update customer",
        operation_description="Update all customer fields.",
        request_body=CustomerSerializer,
        responses={200: CustomerSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete customer",
        operation_description="Delete a customer permanently.",
        responses={204: "Customer deleted successfully"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
