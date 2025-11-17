from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import LeadForm, InteractionFormSet, LeadDetailForm
from django.db.models import OuterRef, Subquery
from django.db.models import OuterRef, Subquery, DateTimeField
from django.db import transaction
from django.db.models.functions import Coalesce
from .models import Lead, Interaction

def lead_list(request):
    # Get filter parameter
    lead_source_filter = request.GET.get('lead_source')
    
    # Base queryset
    leads = Lead.objects.all().order_by('-created_at')
    
    # Apply filter if specified
    if lead_source_filter:
        leads = leads.filter(lead_source=lead_source_filter)
    
    # Get lead source choices for dropdown
    lead_source_choices = Lead.LEAD_SOURCE_CHOICES

    return render(request, 'leads/lead_list.html', {
        'leads': leads,
        'lead_source_choices': lead_source_choices,
        'selected_lead_source': lead_source_filter,
    })


def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    last_interaction = lead.interactions.order_by('-created_at').first()

    if request.method == 'POST':
        detail_form = LeadDetailForm(request.POST)
        if detail_form.is_valid():
            new_status = detail_form.cleaned_data['status']
            note = detail_form.cleaned_data['note']

            with transaction.atomic():
                if new_status and new_status != lead.status:
                    lead.status = new_status
                    lead.save()

                if note:
                    Interaction.objects.create(lead=lead, note=note)

            messages.success(request, 'Perubahan lead berhasil disimpan!')
            return redirect('leads:lead_detail', pk=lead.pk)
    else:
        detail_form = LeadDetailForm(initial={'status': lead.status})

    return render(request, 'leads/lead_detail.html', {
        'lead': lead,
        'detail_form': detail_form,
        'last_interaction': last_interaction
    })


def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        formset = InteractionFormSet(request.POST, instance=Lead())

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                lead = form.save()

                # Re-bind formset to the saved lead to ensure proper relations
                formset = InteractionFormSet(request.POST, instance=lead)
                formset.save()

            messages.success(request, 'Lead berhasil disimpan!')
            return redirect('leads:lead_detail', pk=lead.pk)
    else:
        form = LeadForm()
        formset = InteractionFormSet(instance=Lead())

    return render(request, 'leads/lead_form.html', {'form': form, 'formset': formset, 'lead': None})


def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        formset = InteractionFormSet(request.POST, instance=lead)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                lead = form.save()
                formset.save()
            messages.success(request, 'Lead berhasil disimpan!')
            return redirect('leads:lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)
        formset = InteractionFormSet(instance=lead)

    return render(request, 'leads/lead_form.html', {'form': form, 'formset': formset, 'lead': lead})

