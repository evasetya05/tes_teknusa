from django.shortcuts import render, get_object_or_404, redirect
from post_media.models.channel import Channel, ChannelPerformance
from post_media.forms import ChannelForm
from post_media.models.for_market import Market
from collections import defaultdict
from django.db.models import Prefetch
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from openpyxl import Workbook
from django.http import HttpResponse


def channel_list(request):
    markets = Market.objects.all()
    market_channels = []
    for market in markets:
        channels = Channel.objects.filter(for_market=market)
        if channels.exists():
            grouped_by_channel = {}
            for ch in channels:
                grouped_by_channel.setdefault(ch.channel, []).append(ch)
            # Sort each channel group: unposted (by rencana desc) first, then posted (by tanggal desc)
            for key, ch_list in grouped_by_channel.items():
                unposted = [c for c in ch_list if not c.is_posted]
                posted = [c for c in ch_list if c.is_posted]
                unposted.sort(key=lambda c: (c.rencana_tanggal_posting is not None, c.rencana_tanggal_posting), reverse=True)
                posted.sort(key=lambda c: (c.tanggal_posting is not None, c.tanggal_posting), reverse=True)
                grouped_by_channel[key] = unposted + posted
            market_channels.append({
                'market': market,
                'grouped_channels': grouped_by_channel
            })

    context = {'market_channels': market_channels}
    return render(request, 'post_media/channel_list.html', context)


def channel_detail(request, pk):
    """
    Tampilkan detail channel dan ringkasan performance (tanpa tombol simpan).
    Tiap periode punya link ke halaman update_performance.
    """
    channel = get_object_or_404(Channel, pk=pk)

    # Pastikan tiga periode utama ada
    periods = ['24h', '1w', '1m']
    perf_by_period = {}
    for p in periods:
        perf, _ = ChannelPerformance.objects.get_or_create(
            channel=channel,
            period=p,
            as_of_date=now().date(),
            defaults={'metrics': {}}
        )
        perf_by_period[p] = perf

    context = {
        'channel': channel,
        'performances': perf_by_period,
    }
    return render(request, 'post_media/channel_detail.html', context)


def channel_add(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_media:channel_list')
    else:
        form = ChannelForm()
    return render(request, 'post_media/channel_form.html', {'form': form, 'title': 'Tambah Channel'})

def channel_edit(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            form.save()
            return redirect('post_media:channel_detail', pk=channel.pk)
    else:
        form = ChannelForm(instance=channel)
    return render(request, 'post_media/channel_form.html', {'form': form, 'title': 'Edit Channel'})




def channel_analytics(request):
    """
    Dashboard analytics:
    - Tampilkan semua channel per market.
    - Hanya tampilkan data performance periode '1 Bulan' (period='1m').
    - Bisa difilter berdasarkan market dan jenis channel.
    - Dikelompokkan per channel type dan diurutkan berdasarkan tanggal posting terbaru.
    """
    selected_market = request.GET.get('market')
    selected_channel_type = request.GET.get('channel')

    perf_qs = ChannelPerformance.objects.order_by('-as_of_date')
    qs = Channel.objects.prefetch_related(
        Prefetch('performances', queryset=perf_qs)
    ).select_related('for_market')

    if selected_market:
        qs = qs.filter(for_market__name=selected_market)
    if selected_channel_type:
        qs = qs.filter(channel=selected_channel_type)

    markets = Market.objects.all().order_by('name')

    data_by_market = []
    for market in markets:
        channels = qs.filter(for_market=market)
        if not channels.exists():
            continue

        # --- Pengelompokan per jenis channel ---
        grouped_channels = {}
        for ch in channels:
            grouped_channels.setdefault(ch.channel, []).append(ch)

        # --- Sorting setiap group berdasarkan tanggal posting terbaru ---
        for key in grouped_channels:
            grouped_channels[key].sort(
                key=lambda c: c.tanggal_posting or timezone.datetime.min,
                reverse=True
            )

        # --- Susun data untuk template ---
        channel_data = []
        for channel_type, ch_list in grouped_channels.items():
            for ch in ch_list:
                perf_by_period = {}
                perf_1m = ch.performances.filter(period='1m').order_by('-as_of_date').first()
                if perf_1m:
                    perf_by_period['1 Bulan'] = perf_1m.get_metrics_labeled()

                channel_data.append({
                    'obj': ch,
                    'performances': perf_by_period,
                })

        data_by_market.append({
            'market': market,
            'channels': channel_data,
        })

    context = {
        'markets': markets,
        'selected_market': selected_market,
        'selected_channel_type': selected_channel_type,
        'data_by_market': data_by_market,
    }

    return render(request, 'post_media/channel_analytics.html', context)



def export_channel_analytics_excel(request):
    selected_market = request.GET.get('market')
    selected_channel_type = request.GET.get('channel')

    perf_qs = ChannelPerformance.objects.order_by('-as_of_date')
    qs = Channel.objects.prefetch_related(
        Prefetch('performances', queryset=perf_qs)
    ).select_related('for_market')

    if selected_market:
        qs = qs.filter(for_market__name=selected_market)
    if selected_channel_type:
        qs = qs.filter(channel=selected_channel_type)

    # --- Buat workbook ---
    wb = Workbook()
    ws = wb.active
    ws.title = "Channel Analytics"

    # Header
    headers = [
        "Market", "Judul", "Jenis Konten",
        "Channel", "Tanggal Posting", "Performance (1 Bulan)"
    ]
    ws.append(headers)

    # Data rows
    for ch in qs:
        perf_1m = ch.performances.filter(period='1m').order_by('-as_of_date').first()
        if perf_1m:
            metrics = perf_1m.get_metrics_labeled()
            metrics_str = ", ".join([f"{label}: {value}" for label, value, raw in metrics])
        else:
            metrics_str = "Tidak ada data"

        ws.append([
            ch.for_market.name if ch.for_market else "",
            ch.judul,
            ch.jenis_konten,
            ch.channel,
            ch.tanggal_posting.strftime("%d-%m-%Y") if ch.tanggal_posting else "",
            metrics_str,
        ])

    # --- Styling ringan opsional ---
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    # --- Response ---
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="channel_analytics.xlsx"'
    wb.save(response)
    return response

def update_performance(request, pk):
    channel = get_object_or_404(Channel, pk=pk)

    # Semua periode yang kita dukung
    periods = ['24h', '1w', '1m']

    # Daftar metric sesuai channel
    CHANNEL_METRICS = {
        'ig': ['views', 'view_f', 'view_nf', 'account_reached', 'interaction', 'profile'],
        'threads': ['impressions', 'likes', 'replies', 'reposts'],
        'linkedin': ['impressions', 'reactions', 'comments', 'shares'],
        'linkedin_newsletter': ['impressions', 'member_reached', 'profile_activity', 'views', 'social_engagement'],
        'linkedin_company': ['impressions', 'member_reached', 'engagement', 'clicks', 'reactions', 'comments', 'repost'],
        'tiktok': ['views', 'hearts', 'comments', 'shares'],
        'blog': ['views', 'comments', 'clicks'],
    }

    ##
    # Simpan performance tiap periode
    performances = {}
    for p in periods:
        perf, _ = ChannelPerformance.objects.get_or_create(
            channel=channel,
            period=p,
            as_of_date=now().date(),
            defaults={'metrics': {}}
        )
        performances[p] = perf

    # Jika form dikirim
    if request.method == 'POST':
        period = request.POST.get('period')
        perf = performances.get(period)
        if perf:
            metrics = perf.metrics or {}

            # Pilih metric list berdasarkan channel
            metric_fields = CHANNEL_METRICS.get(channel.channel, ['views', 'impressions', 'likes', 'reactions', 'comments', 'shares'])

            for field in metric_fields:
                if field in request.POST:
                    try:
                        metrics[field] = int(request.POST[field])
                    except ValueError:
                        continue

            perf.metrics = metrics
            perf.save()
        return redirect('post_media:channel_detail', pk=channel.pk)

    context = {
        'channel': channel,
        'performances': performances,
        'metric_fields': CHANNEL_METRICS.get(channel.channel, ['views', 'impressions', 'likes', 'reactions', 'comments', 'shares']),
    }
    return render(request, 'post_media/update_performance.html', context)
