from django.contrib import admin
from .models import Notification

@admin.register(Notification)
# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "message","is_read","created_at")
    list_filter = ("user", "is_read","created_at")