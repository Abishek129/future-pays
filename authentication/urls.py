# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')
urlpatterns = [
    path('verify_token/', verify_token, name='verify_token'),

    path('login/', login_user),
    path('', include(router.urls)),
    path('update-profile/', update_user_profile, name='update_profile'),
    path('referal-admin/', AdminReferralCreateView.as_view(), name = 'referral-admin'),
    path('google-signup/', GoogleSignupAPIView.as_view(), name="google signup"),
    path('google-signin/', GoogleSigninAPIView.as_view(), name="google signin")
]
