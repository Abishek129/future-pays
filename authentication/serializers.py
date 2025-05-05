from rest_framework import serializers
from .models import Address, Referral

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']  # Ensure user is assigned from request


class AdminReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['user']  # Admins only provide the user; referral_code auto-generates

        
