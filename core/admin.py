from django.contrib import admin
from .models import Job, Category, Proposal
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "budget", "job_type", "is_assigned", "is_completed", "escrow_released", "created_at")
    list_filter = ("job_type", "is_assigned", "is_completed", "escrow_released", "created_at")
    search_fields = ("title", "client__email", "description", "short_description")
    autocomplete_fields = ("client", "freelancer", "categories")
    filter_horizontal = ("categories",)
    date_hierarchy = "created_at"
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_category")
    search_fields = ("name",)
    
@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("freelancer", "job__title", "bid_amount", "submitted_at","accepted")