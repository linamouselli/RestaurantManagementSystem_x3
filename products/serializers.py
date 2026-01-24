from .models import Category, Product
from rest_framework import serializers
from django.core.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' ,'description', 'is_active']

    def validate(self, attrs):
        category = Category(**attrs)
        try:
            category.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = Product
        fields = ['id', 'name','description' , 'price', 'category', 'category_id' , 'is_available', 'preparation_time']

    def validate(self, attrs):
        product = Product(**attrs)
        try:
            product.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs
