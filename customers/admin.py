from django.contrib import admin
from .models import Cart, global_pool, Notifications
# Register your models here.

admin.site.register(Cart)
admin.site.register(global_pool)
admin.site.register(Notifications)
