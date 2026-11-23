from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['type', 'title', 'description', 'location', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }