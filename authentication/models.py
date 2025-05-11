from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta


from django.core.files.storage import FileSystemStorage
from PIL import Image
import os

def user_image_path(instance, filename):
    gmail = instance.email.split('@')[0]
    return f'dp/{gmail}/{filename}'
# ================================
# User Manager
# ================================
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # Important for Google Sign-In
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# ================================
# User Model
# ================================
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]
    image = models.ImageField(
        upload_to=user_image_path,
        default='default_dp.webp',
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True)
    firebase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)  # ✅ Replace first_name & last_name
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    reset_token = models.CharField(max_length=128, blank=True, null=True)
    reset_token_created_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

from django.conf import settings

class Address(models.Model):
    """
    Represents a user's address for checkout and profile management.
    """
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('others', 'Others'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="addresses"
    )

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    locality = models.CharField(max_length=255)
    flat_number = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="India")  # Default to India
    is_default = models.BooleanField(default=False)
    latitude = models.DecimalField(blank = True,null=True, decimal_places=4, max_digits=8)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address_mode = models.CharField(
        max_length=15,
        choices=ADDRESS_TYPE_CHOICES,
        default='home',
        help_text="modes of address"
    )

    def save(self, *args, **kwargs):
        """
        Ensure only one address is marked as default.
        """
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}, {self.city}, {self.country}"
    
import uuid
from django.db import models, IntegrityError, transaction
from django.conf import settings

from django.contrib.auth import get_user_model

def get_default_admin():
    User = get_user_model()
    return User.objects.filter(is_staff=True).first()

def get_default_admin():
    User = get_user_model()
    return User.objects.filter(is_staff=True).first()



def generate_unique_referral_code():
    for _ in range(5):
        code = str(uuid.uuid4()).replace('-', '')[:10]
        if not Referral.objects.filter(referral_code=code).exists():
            return code
    raise Exception("Failed to generate unique referral code after 5 attempts.")

class Referral(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="referral_code"
    )
    referral_code = models.CharField(
        max_length=10, 
        unique=True, 
        blank=True, 
        null=True
    )
    referred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="referrals",
        default=get_default_admin,
        null=True,  # Allow NULL values for admins
        blank=True # Sets referred_by to first admin
    )
    referred_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_unique_referral_code()
        super().save(*args, **kwargs)




class CustomerPool(models.Model):
    owner =  models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="pool"
    )
    token = models.BigIntegerField(default=-1)
    is_active = models.BooleanField(default=True)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, blank=True)













        


