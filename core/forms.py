from django import forms
from .models import Job, Proposal

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

class JobProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [
            'message',
            'bid_amount',
        ]