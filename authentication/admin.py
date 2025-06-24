from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'profile_picture', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'gender')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'profile_picture', 'crypto_wallet_address')}),
        ('Permissions', {'fields': ('role', 'is_freelancer', 'is_client', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'gender', 'role', 'profile_picture', 'is_freelancer', 'is_client', 'password1', 'password2'),
        }),
    )
