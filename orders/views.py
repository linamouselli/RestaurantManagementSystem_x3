from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['customer', 'status']
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['New', 'Preparing', 'Ready', 'Delivered']:
            order.status = new_status
            order.save()
            return Response({'status': 'updated'})
        return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
