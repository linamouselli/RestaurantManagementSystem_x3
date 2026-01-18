from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_amount', 'notes', 'items']
        read_only_fields = ['total_amount']

    def validate_items(self, value):
        for item in value:
            if not item['product'].is_available:
                raise serializers.ValidationError(f"{item['product'].name} unavailable")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items_data:
            product = item['product']
            OrderItem.objects.create(order=order, product=product, quantity=item['quantity'],
                                     price_at_order=product.price)
            total += product.price * item['quantity']

        order.total_amount = total
        order.save()
        return order