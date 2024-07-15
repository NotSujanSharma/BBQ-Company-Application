from django import forms
from .models import Campaign, Staff

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'subject', 'content', 'recipient_group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded px-3 py-2'}),
            'subject': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded px-3 py-2'}),
            'content': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded px-3 py-2', 'rows': 6}),
            'recipient_group': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white rounded px-3 py-2'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'role', 'phone', 'address', 'joined_at']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'role': forms.Select(),
            'phone': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 4}),
            'joined_at': forms.DateInput(attrs={'type': 'date'}),
        }