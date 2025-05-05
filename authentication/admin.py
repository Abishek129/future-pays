from django.contrib import admin
from .models import Referral
from django.contrib import admin
from .models import *

# ================================
# User Admin
# ================================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'user_type', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('date_joined',)


admin.site.register(Referral)
admin.site.register(CustomerPool)
admin.site.register(Address)