from django.shortcuts import render, get_object_or_404, redirect
from .forms import LeadForm, InteractionForm, InteractionFormSet
from django.db.models import OuterRef, Subquery
from django.db.models import OuterRef, Subquery, DateTimeField
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
    
    # Ambil interaksi terakhir
    last_interaction = lead.interactions.order_by('-created_at').first()

    if request.method == 'POST':
        # Cek jika user ubah status
        if 'change_status' in request.POST:
            new_status = request.POST.get('status')
            if new_status in dict(Lead.STATUS_CHOICES):
                lead.status = new_status
                lead.save()
                return redirect('leads:lead_detail', pk=lead.pk)

        # Cek jika user tambah interaksi
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.lead = lead
            interaction.save()
            return redirect('leads:lead_detail', pk=lead.pk)
    else:
        form = InteractionForm()

    return render(request, 'leads/lead_detail.html', {
        'lead': lead,
        'form': form,
        'last_interaction': last_interaction
    })


def lead_create(request, pk=None):
    if pk:
        lead = get_object_or_404(Lead, pk=pk)
    else:
        lead = None

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        formset = InteractionFormSet(request.POST, instance=lead)
        if form.is_valid() and formset.is_valid():
            lead = form.save()
            formset.save()
            return redirect('leads:lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)
        formset = InteractionFormSet(instance=lead)

    return render(request, 'leads/lead_form.html', {'form': form, 'formset': formset, 'lead': lead})

