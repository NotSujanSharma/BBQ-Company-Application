from django import forms
from .models import Campaign

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
