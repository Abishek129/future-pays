from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()
import firebase_admin
from firebase_admin import auth, credentials
from .models import CustomerPool




User = get_user_model()

def get_default_admin():
    return User.objects.filter(is_staff=True).first()

def generate_unique_referral_code():
    import uuid
    for _ in range(5):
        code = str(uuid.uuid4()).replace('-', '')[:10]
        if not Referral.objects.filter(referral_code=code).exists():
            return code
    raise Exception("Failed to generate unique referral code after 5 attempts.")







# Address APIs


from rest_framework import viewsets, permissions
from .models import Address, Referral
from .serializers import AddressSerializer, AdminReferralSerializer

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserAddressListAPIView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import os
from django.core.files.storage import default_storage
from django.conf import settings

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_user_profile(request):
    user = request.user
    name = request.data.get("name")
    phone_number = request.data.get("phone_number")
    image_file = request.FILES.get("image")

    if name:
        user.name = name
    if phone_number:
        user.phone_number = phone_number

    if image_file:
        email_prefix = user.email.split('@')[0]
        dp_path = f"dp/{email_prefix}/"
        os.makedirs(os.path.join(settings.MEDIA_ROOT, dp_path), exist_ok=True)

        new_path = os.path.join(dp_path, "profile_image.webp")
        full_path = os.path.join(settings.MEDIA_ROOT, new_path)

        # Convert and save image as webp
        img = Image.open(image_file)
        img.convert("RGB").save(full_path, "webp")

        user.image.name = new_path

    user.save()
    return Response({
        "status": "success",
        "message": "User profile updated"
    }, status=status.HTTP_200_OK)




from rest_framework import generics, permissions

class AdminReferralCreateView(generics.CreateAPIView):
    queryset = Referral.objects.all()
    serializer_class = AdminReferralSerializer
    
    def create(self, request, *args, **kwargs):
        # Get the authenticated admin user from the Bearer token
        admin_user = request.user

        # Deserialize the incoming data

        
        # Save referral with referred_by=None (admin created)
        referral = Referral.objects.create(
            user=admin_user,
            referred_by=None
        )

        return Response(
            {
                "message": "Referral created successfully",
                "referral_id": referral.id,
                "referred_user": referral.user.email,
                "created_by_admin": admin_user.email
            },
            status=status.HTTP_201_CREATED
        )
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import traceback

class GoogleSignupAPIView(APIView):
    def post(self, request):
        try:
            id_token_from_client = request.data.get('id_token')
            input_referral_code = request.data.get("referral_code")
            id_info = id_token.verify_oauth2_token(
                id_token_from_client,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = id_info['email']
            name = id_info.get('name', '')
            picture = id_info.get('picture', '')
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with email already exists"}, status=400)

            user = User.objects.create(email=email)

            
            user.set_unusable_password()
            user.save()

            refresh = RefreshToken.for_user(user)

            if input_referral_code:
                try:
                    referred_by = Referral.objects.get(referral_code=input_referral_code).user
                except Referral.DoesNotExist:
                    return JsonResponse({"error": "Invalid referral code."}, status=400)
            else:
                referred_by = get_default_admin()

            # Create referral
            Referral.objects.create(
                user=user,
                referred_by=referred_by,
                referral_code=generate_unique_referral_code()
            )

            # Create customer pool
            CustomerPool.objects.create(
                owner=user  # Assign the signed-up user
                # All other fields take default values
            )
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'name': user.name,
                    'user_type': user.user_type,
                    'image': user.image.url if user.image else '',
                }
            })

        except Exception as e:
            print("===== GOOGLE SIGNUP ERROR =====")
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)



class GoogleSigninAPIView(APIView):
    def post(self, request):
        try:
            id_token_from_client = request.data.get('id_token')
            #input_referral_code = request.data.get("referral_code")
            id_info = id_token.verify_oauth2_token(
                id_token_from_client,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = id_info['email']
            name = id_info.get('name', '')
            picture = id_info.get('picture', '')
            if not User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with email doesnot  exists"}, status=400)

            user= User.objects.get(email=email)

            

            refresh = RefreshToken.for_user(user)

            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'name': user.name,
                    'user_type': user.user_type,
                    'image': user.image.url if user.image else '',
                }
            })

        except Exception as e:
            print("===== GOOGLE SIGNUP ERROR =====")
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)