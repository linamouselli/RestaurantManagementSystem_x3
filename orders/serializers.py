from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product' , 'product_name',  'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer','order_date' , 'status', 'total_amount', 'notes', 'items']

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


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        allowed = ['New', 'Preparing', 'Ready', 'Delivered']
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of {allowed}"
            )

        order = self.instance
        if order:
            current_index = allowed.index(order.status)
            new_index = allowed.index(value)

            if new_index != current_index + 1:
                raise serializers.ValidationError(
                    f"Status must progress step by step: {order.status} → {value}"
                )

        return value