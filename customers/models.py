from django.db import models
from products.models import Product, Size
#from django.contrib.auth import get_user_model
from django.conf import settings
from authentication.models import Address

#User = get_user_model


from django.db import models
from django.conf import settings
from products.models import Product, Size

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='in_carts'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name='in_carts'
    )
    payable_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        if not self.payable_amount:
            self.payable_amount = self.product.offer_price  # or base_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.product} ({self.size})"
    


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    ORDER_STATUS_CHOICES = [
        ('created', 'Created'),
        ('placed', 'Order Placed'),      
        ('shipped', 'Shipped'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    payable_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    address = models.ForeignKey(
        Address,
        related_name="orders",
        on_delete=models.CASCADE
    )
    payment_status = models.CharField(
        max_length=15,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        help_text="Payment status for the order."
    )
    order_status = models.CharField(
        max_length=15,
        choices=ORDER_STATUS_CHOICES,
        default='created',
        help_text="Current status of the order."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class global_pool(models.Model):
    start = models.BigIntegerField(default=2)
    end = models.BigIntegerField(default=1)
    pool_amount = models.DecimalField(max_digits=50, decimal_places=2, default= 0.00)
    total_window_amount = models.DecimalField(max_digits=50, decimal_places=2, blank=True)
    counter = models.IntegerField(default=1)
    latest = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total_window_amount = 200 * (2**self.counter)
        super().save(*args, **kwargs)




from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"To: {self.user.full_name} | {self.message[:30]}"
