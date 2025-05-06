from django.contrib import admin
from .models import Cart, global_pool
# Register your models here.

admin.site.register(Cart)
admin.site.register(global_pool)
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'seen')
    list_filter = ('seen', 'timestamp')
