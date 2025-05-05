from django.db import models
from django.contrib.auth import get_user_model
#from vendors.models import VendorDetails
from django.utils.text import slugify
#from django.contrib.postgres.fields import ArrayField
from PIL import Image
import os
from django.conf import settings
#from .utils import generate_vector
#from pgvector.django import VectorField

User = get_user_model()


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    #slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)
    #slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        unique_together = ('attribute', 'value')

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

# ================================
# Product Model
# ================================
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Product(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True, help_text="Detailed product description")

    additional_details = models.JSONField(blank=True, null=True, help_text="Structured additional details for the product")

    is_active = models.BooleanField(default=True)

    cancellation_stage = models.CharField(
        max_length=50,
        choices=[
            ('before_packing', 'Before Packing'),
            ('before_shipping', 'Before Shipping'),
            ('before_delivery', 'Before Delivery'),
        ],
        blank=True,
        null=True,
        help_text="Stage at which cancellation is allowed"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0)

    

    def update(self, instance, validated_data):
        images_data = self.initial_data.getlist('images') if hasattr(self.initial_data, 'getlist') else self.initial_data.get('images', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data:
            instance.images.all().delete()  # optional: replace existing
            for img in images_data:
                ProductImage.objects.create(product=instance, image=img)
        return instance


    def save(self,  *args, **kwargs):
        if self.offer_price == 0 and self.base_price != 0:
            self.offer_price == self.base_price
        super().save( *args, **kwargs)
    def __str__(self):
        return self.name

# ================================
# Product Variant Modell
# ================================




# ================================
# Product Image Model
# ================================
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._convert_image_to_jpeg()

    def _convert_image_to_jpeg(self):
        if self.image:
            try:
                input_path = self.image.path
                output_path = f"{os.path.splitext(input_path)[0]}.jpeg"
                if not os.path.exists(output_path):
                    with Image.open(input_path) as img:
                        img = img.convert('RGB')
                        img.save(output_path, 'JPEG', quality=85)
                    self.image.name = os.path.relpath(output_path, settings.MEDIA_ROOT)
                    super().save(update_fields=['image'])
            except Exception as e:
                print(f"Error converting image to JPEG: {e}")

    def __str__(self):
        return f"Image for {self.product.name}"
    

from django.db import models

class Size(models.Model):
    SIZE_CHOICES = [
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
    ]

    label = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        unique=True,
        default="s",
        help_text="Allowed sizes: S, M, L, XL, etc."
    )

    def __str__(self):
        return self.get_label_display()
