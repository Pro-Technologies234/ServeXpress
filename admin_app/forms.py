from django import forms
from authentication.models import User
from core.models import Job, Proposal


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "gender", "role", "crypto_wallet_address"]
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "gender", "role", "crypto_wallet_address", "password"]
        

class PostJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'short_description',
            'job_type',
            'budget',
        ]
    
class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "short_description", "budget"]
        
    title = forms.CharField(max_length=255)
    short_description = forms.CharField(max_length=255)
    description = forms.Textarea()
    
    budget = forms.DecimalField(max_digits=10, decimal_places=2)
    
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['client', 'created_at', 'is_assigned', 'is_completed', 'freelancer', 'escrow_released']

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ['freelancer', 'submitted_at', 'accepted']    