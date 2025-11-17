from django import forms
from django.forms import inlineformset_factory
from .models import Lead, Interaction

class LeadForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'account_medsos', 'lead_source', 'assigned_to', 'priority', 'estimated_value', 'next_follow_up', 'status']
        widgets = {
            'estimated_value': forms.NumberInput(attrs={'step': '0.01'}),
            'next_follow_up': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget

            # Ensure date inputs have correct type
            if isinstance(widget, forms.DateInput):
                widget.attrs.setdefault('type', 'date')

            # Apply Bootstrap form classes
            if isinstance(widget, (forms.Select, forms.SelectMultiple, forms.CheckboxSelectMultiple)):
                base_class = 'form-select'
            elif isinstance(widget, (forms.CheckboxInput,)):
                base_class = 'form-check-input'
            else:
                base_class = 'form-control'

            existing_classes = widget.attrs.get('class', '')
            widget.attrs['class'] = f"{existing_classes} {base_class}".strip()

            # Add placeholder for text inputs where appropriate
            if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Textarea)):
                widget.attrs.setdefault('placeholder', field.label)

            # Highlight invalid fields when bound
            if self.is_bound and name in self.errors:
                widget.attrs['class'] = f"{widget.attrs['class']} is-invalid".strip()

InteractionFormSet = inlineformset_factory(Lead, Interaction, fields=['note'], extra=1, can_delete=True)

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            existing_classes = widget.attrs.get('class', '')
            widget.attrs['class'] = f"{existing_classes} form-control".strip()

            if self.is_bound and name in self.errors:
                widget.attrs['class'] = f"{widget.attrs['class']} is-invalid".strip()

            field.required = False


class LeadDetailForm(forms.Form):
    status = forms.ChoiceField(choices=Lead.STATUS_CHOICES)
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Catatan Interaksi')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.Select):
                base_class = 'form-select'
            else:
                base_class = 'form-control'

            existing_classes = widget.attrs.get('class', '')
            widget.attrs['class'] = f"{existing_classes} {base_class}".strip()

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault('placeholder', 'Tambahkan catatan interaksi (opsional)')
