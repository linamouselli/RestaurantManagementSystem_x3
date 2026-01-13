from .models import Category, Product
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' ,'description', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','description' , 'price', 'category', 'is_available', 'preparation_time']
