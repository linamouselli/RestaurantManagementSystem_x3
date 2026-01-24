from django.shortcuts import render
from rest_framework import viewsets, filters

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import IsAdmin, IsManager, IsAdminOrManager, IsStaff
from drf_spectacular.utils import extend_schema, extend_schema_view

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="List all categories",
        description="Retrieve a list of all categories of our products.",
        responses={200: CategorySerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get category details",
        description="Retrieve details of a specific category by ID.",
    ),
    create=extend_schema(
        summary="Create a new category",
        description="Add a new category of products to our restaurant.",
    ),
    update=extend_schema(
        summary="Update a category",
        description="Update all fields of a specific category.",
    ),
    destroy=extend_schema(
        summary="Delete a category",
        description="Remove a category from the restaurant.",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminOrManager()]


@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Retrieve a list of all products of our restaurant menu.",
        responses={200: ProductSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get product details",
        description="Retrieve details of a specific product by ID.",
    ),
    create=extend_schema(
        summary="Create a new product",
        description="Add a new product to the restaurant menu.",
    ),
    update=extend_schema(
        summary="Update a product",
        description="Update all fields of a specific product.",
    ),
    destroy=extend_schema(
        summary="Delete a product",
        description="Remove a product from the restaurant menu.",
    ),
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__name', 'price']
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'available_products']:
            return [AllowAny()]
        return [IsAdminOrManager()]


    @action(detail=False, methods=['get'], url_path='available')
    def available_products(self, request):
        available = Product.objects.filter(is_available=True)
        page = self.paginate_queryset(available)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)



