

from rest_framework import serializers
from .models import Cart, Order, global_pool

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product', 'size', 'payable_amount']
        read_only_fields = ['payable_amount']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',               # read-only, auto-assigned from request.user
            'product',
            'size',
            'payable_amount',     # read-only, ideally set from product price
            'address',
            'payment_status',
            'order_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'user',
            'payable_amount',
            'created_at',
            'updated_at'
        ]


# serializers.py
from rest_framework import serializers
from .models import Notifications

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'message', 'seen', 'timestamp', 'title']
