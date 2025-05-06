# serializers.py
from rest_framework import serializers
from .models import Attribute, AttributeValue, ProductImage, Product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute', 'value']  # Add 'slug' if using

class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']  # Add 'slug' if using


class ProductSerializer(serializers.ModelSerializer):
    
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            
            'additional_details',
            'is_active',
            
            'cancellation_stage',
            'base_price',
            'offer_price',
            
            
            'created_at',
            'updated_at',
            'images',  # Included here
        ]
        read_only_fields = ['created_at', 'updated_at']




from rest_framework import serializers
from .models import Size

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'label']
