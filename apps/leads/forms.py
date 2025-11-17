from django import forms
from django.forms import inlineformset_factory
from .models import Lead, Interaction

class LeadForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'account_medsos', 'lead_source', 'assigned_to', 'priority', 'estimated_value', 'next_follow_up', 'status']

InteractionFormSet = inlineformset_factory(Lead, Interaction, fields=['note'], extra=1, can_delete=True)

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['note']
