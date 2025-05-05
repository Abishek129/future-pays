from customers.models import global_pool
from rest_framework import serializers



class GlobalPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = global_pool
        fields = '__all__'