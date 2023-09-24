from django import forms
from .models import LeadUser


class LeadUserForm(forms.ModelForm):
    class Meta:
        model = LeadUser
        fields = ['full_name', 'phone', 'age', 'location']
