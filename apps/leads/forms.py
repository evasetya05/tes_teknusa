from django import forms
from .models import Lead, Interaction

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'lead_source', 'assigned_to', 'priority', 'estimated_value', 'next_follow_up', 'general_notes', 'status']

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['note']
