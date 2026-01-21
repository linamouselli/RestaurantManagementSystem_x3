from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from orders.models import Order
from orders.serializers import OrderSerializer
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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['customer', 'status']
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['put'], permission_classes=[IsAdminOrManager()])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['New', 'Preparing', 'Ready', 'Delivered']:
            order.status = new_status
            order.save()
            return Response({'status': 'updated'})
        return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response({'error': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(customer_id=customer_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
