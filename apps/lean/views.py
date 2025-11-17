# lean/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Idea, Build, Product, Measure, DataPoint, Learning
from .forms import IdeaForm, BuildForm, ProductForm, MeasureForm, DataPointForm, LearningForm

# === Idea Views ===
class IdeaListView(generic.ListView):
    model = Idea
    template_name = 'lean/idea_list.html'
    context_object_name = 'ideas'
    paginate_by = 20

class IdeaDetailView(generic.DetailView):
    model = Idea
    template_name = 'lean/idea_detail.html'


def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save()
            return redirect(idea.get_absolute_url())
    else:
        form = IdeaForm()
    return render(request, 'lean/item_form.html', {'form': form, 'title': 'Create Idea'})


def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            return redirect(idea.get_absolute_url())
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'lean/item_form.html', {'form': form, 'title': f'Edit Idea: {idea.title}'})

# === Generic item edit pattern ===
def item_edit(request, model, form_class, pk, parent_field=None, redirect_to=None):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            elif parent_field:
                parent = getattr(obj, parent_field)
                return redirect(parent.get_absolute_url())
            else:
                return redirect(obj.get_absolute_url())
    else:
        form = form_class(instance=obj)
    return render(request, 'lean/item_form.html', {'form': form, 'title': f'Edit {model.__name__}: {obj}'})


# Shortcut views
def build_edit(request, pk):
    return item_edit(request, Build, BuildForm, pk, parent_field='idea')

def product_edit(request, pk):
    return item_edit(request, Product, ProductForm, pk, parent_field='build')

def measure_edit(request, pk):
    return item_edit(request, Measure, MeasureForm, pk, parent_field='product')

def datapoint_edit(request, pk):
    return item_edit(request, DataPoint, DataPointForm, pk, parent_field='measure')

def learning_edit(request, pk):
    return item_edit(request, Learning, LearningForm, pk, parent_field='idea')
