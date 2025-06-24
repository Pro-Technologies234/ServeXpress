from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

User = settings.AUTH_USER_MODEL

# Create your models here.
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    rating = models.FloatField(default=0.0)
    completed_jobs = models.IntegerField(default=0)

    def _str_(self):
        return f"{self.user.username}'s Profile"
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey("self",on_delete=models.CASCADE,related_name="sub_categories", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    


class Job(models.Model):
    JOB_TYPE = [
        ("remote","Remote"),
        ("on-site","On-site"),
        ("hybrid","Hybrid"),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    categories = models.ManyToManyField(Category, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=255,blank=True)
    job_type = models.CharField(choices=JOB_TYPE,max_length=15,blank=True,null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_assigned = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    freelancer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taken_jobs')
    escrow_released = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.title} by {self.client.email}"
    
class Proposal(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='proposals')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def _str_(self):
        return f"Proposal by {self.freelancer.username} for {self.job.title}"
    
class DeliveryRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_requests')
    pickup_address = models.TextField()
    dropoff_address = models.TextField()
    country = CountryField()
    package_details = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_tasks')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    is_picked_up = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    escrow_released = models.BooleanField(default=False)

    def _str_(self):
        return f"Delivery by {self.client.username} to {self.dropoff_address}"
    

class QRScan(models.Model):
    delivery = models.ForeignKey(DeliveryRequest, on_delete=models.CASCADE, related_name='qr_scans')
    scanned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    scan_type = models.CharField(max_length=20, choices=[('pickup', 'Pickup'), ('dropoff', 'Dropoff')])

    def _str_(self):
        return f"{self.scan_type.capitalize()} scan by {self.scanned_by.username}"
    

class CryptoPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    delivery = models.ForeignKey(DeliveryRequest, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)  # e.g., USDT, BTC
    transaction_id = models.CharField(max_length=128)
    status = models.CharField(max_length=50, default="pending")  # pending, confirmed, failed
    created_at = models.DateTimeField(auto_now_add=True)
    escrow_held = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.currency} - {self.amount} by {self.user.username}"
    
    
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    delivery = models.ForeignKey(DeliveryRequest, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Review for {self.freelancer.username} ({self.rating})"
    
    
class Dispute(models.Model):
    opened_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    delivery = models.ForeignKey(DeliveryRequest, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)
    admin_decision = models.CharField(max_length=50, blank=True, null=True)  # refund, partial, release

    def _str_(self):
        return f"Dispute by {self.opened_by.email}"
    