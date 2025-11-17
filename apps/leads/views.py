from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from .forms import LeadForm, InteractionFormSet, LeadDetailForm
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
            messages.error(request, 'Gagal menyimpan lead baru. Periksa kembali isian formulir.')
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
            messages.error(request, 'Gagal menyimpan perubahan lead. Silakan periksa kembali isian Anda.')
    else:
        form = LeadForm(instance=lead)
        formset = InteractionFormSet(instance=lead)

    return render(request, 'leads/lead_form.html', {'form': form, 'formset': formset, 'lead': lead})


def lead_analysis(request):
    total_leads = Lead.objects.count()
    active_leads = Lead.objects.exclude(status__in=['won', 'lost']).count()
    won_leads = Lead.objects.filter(status='won').count()

    conversion_rate = (won_leads / total_leads * 100) if total_leads else 0

    today = timezone.localdate()
    pending_followups = Lead.objects.filter(
        next_follow_up__gte=today,
        status__in=['new', 'contacted', 'qualified', 'proposal_sent', 'negotiation']
    ).count()
    overdue_followups = Lead.objects.filter(
        next_follow_up__lt=today,
        status__in=['new', 'contacted', 'qualified', 'proposal_sent', 'negotiation']
    ).count()

    status_counts = (
        Lead.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    status_display = dict(Lead.STATUS_CHOICES)
    breakdown_status = [
        {
            'key': item['status'],
            'label': status_display.get(item['status'], item['status']),
            'count': item['count'],
            'percentage': (item['count'] / total_leads * 100) if total_leads else 0,
        }
        for item in status_counts
    ]

    source_counts = (
        Lead.objects.values('lead_source')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    source_display = dict(Lead.LEAD_SOURCE_CHOICES)
    breakdown_sources = [
        {
            'key': item['lead_source'] or '-',
            'label': source_display.get(item['lead_source'], 'Tidak diketahui'),
            'count': item['count'],
        }
        for item in source_counts
        if item['lead_source'] or item['count']
    ]

    recent_leads = Lead.objects.order_by('-created_at')[:8]
    recent_interactions = (
        Interaction.objects.select_related('lead')
        .order_by('-created_at')[:8]
    )

    context = {
        'metrics': {
            'total_leads': total_leads,
            'active_leads': active_leads,
            'won_leads': won_leads,
            'conversion_rate': conversion_rate,
            'pending_followups': pending_followups,
            'overdue_followups': overdue_followups,
        },
        'breakdown': {
            'status': breakdown_status,
            'sources': breakdown_sources,
        },
        'recent_leads': recent_leads,
        'recent_interactions': recent_interactions,
    }

    return render(request, 'leads/lead_analisis.html', context)
def lead_graphic(request):
    # Similar to lead_analysis but for graphics
    from datetime import timedelta
    from django.db.models.functions import TruncDate
    
    total_leads = Lead.objects.count()
    active_leads = Lead.objects.exclude(status__in=['won', 'lost']).count()
    won_leads = Lead.objects.filter(status='won').count()
    
    status_counts = Lead.objects.values('status').annotate(count=Count('id')).order_by('-count')
    source_counts = Lead.objects.values('lead_source').annotate(count=Count('id')).order_by('-count')
    
    status_display = dict(Lead.STATUS_CHOICES)
    source_display = dict(Lead.LEAD_SOURCE_CHOICES)
    
    breakdown_status = [{'key': item['status'], 'label': status_display.get(item['status'], item['status']), 'count': item['count'], 'percentage': (item['count'] / total_leads * 100) if total_leads else 0} for item in status_counts]
    breakdown_sources = [{'key': item['lead_source'] or '-', 'label': source_display.get(item['lead_source'], 'Tidak diketahui'), 'count': item['count']} for item in source_counts if item['lead_source'] or item['count']]
    
    start_date = timezone.localdate() - timedelta(days=13)
    leads_by_day = Lead.objects.filter(created_at__date__gte=start_date).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
    interactions_by_day = Interaction.objects.filter(created_at__date__gte=start_date).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
    
    leads_map = {item['day']: item['count'] for item in leads_by_day}
    interactions_map = {item['day']: item['count'] for item in interactions_by_day}
    
    labels = []
    lead_counts_series = []
    interaction_counts_series = []
    
    for idx in range(14):
        current_day = start_date + timedelta(days=idx)
        labels.append(current_day.strftime('%d %b'))
        lead_counts_series.append(leads_map.get(current_day, 0))
        interaction_counts_series.append(interactions_map.get(current_day, 0))
    
    context = {
        'metrics': {'total_leads': total_leads, 'active_leads': active_leads, 'won_leads': won_leads},
        'breakdown': {'status': breakdown_status, 'sources': breakdown_sources},
        'charts': {'labels': labels, 'lead_counts': lead_counts_series, 'interaction_counts': interaction_counts_series},
    }
    
    return render(request, 'leads/lead_graphic.html', context)
