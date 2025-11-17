from django import forms
from .models import Idea, Build, Product, Measure, DataPoint, Learning

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'assumptions', 'priority', 'status']

class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ['title', 'description', 'link', 'status']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'public']

class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ['metric', 'target', 'current', 'notes']

class DataPointForm(forms.ModelForm):
    class Meta:
        model = DataPoint
        fields = ['value', 'measured_at', 'note']

class LearningForm(forms.ModelForm):
    class Meta:
        model = Learning
        fields = ['summary', 'action']
