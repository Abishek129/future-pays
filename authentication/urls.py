# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')
urlpatterns = [

    path('', include(router.urls)),
    path('update-profile/', update_user_profile, name='update_profile'),
    path('user/address/', UserAddressListAPIView.as_view(), name = "user-address"),
    path('referal-admin/', AdminReferralCreateView.as_view(), name = 'referral-admin'),
    path('google-signup/', GoogleSignupAPIView.as_view(), name="google signup"),
    path('google-signin/', GoogleSigninAPIView.as_view(), name="google signin"),
    path('facebook-login/', FacebookLoginView.as_view(), name = 'facebook-login' ),
    path('facebook-signup/', FacebookSignupView.as_view(), name = 'facebook-signup'),
    path('email-change/', ChangemailView.as_view(), name = "email-change"),

]
