from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from orders.models import Order
from orders.serializers import OrderSerializer, OrderStatusSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsManager, IsStaff, IsAdminOrManager
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="List all orders",
        description="Retrieve a list of all orders of all customers.",
        responses={200: OrderSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get order details",
        description="Retrieve details of a specific order by ID.",
    ),
    create=extend_schema(
        summary="Create a new order",
        description="Make a new order with delicious products that our restaurant offers.",
    ),
    update=extend_schema(
        summary="Update an order",
        description="Update details of a specific order.",
    ),
    destroy=extend_schema(
        summary="Delete an order",
        description="Remove an order.",
    ),
)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    filterset_fields = ['customer', 'status']
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    @action(
        detail=True,
        methods=['put'],
        permission_classes=[IsAdminOrManager],
        url_path='status'
    )
    def status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Order status updated successfully",
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )