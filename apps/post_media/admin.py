from django.contrib import admin
from post_media.models import Channel, ChannelPerformance


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        'judul', 'channel', 'akun', 'for_market', 
        'funnel_stage', 'kategori_biaya', 
        'rencana_tanggal_posting', 'tanggal_posting', 'is_posted'
    )
    list_filter = ('akun', 'channel', 'funnel_stage', 'is_posted', 'for_market')
    search_fields = ('judul', 'jenis_konten', 'kategori_biaya')
    date_hierarchy = 'tanggal_posting'
    ordering = ('-tanggal_posting',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('judul', 'jenis_konten', 'isi_konten')
        }),
        ('Detail Channel', {
            'fields': ('akun', 'for_market', 'channel', 'funnel_stage', 'kategori_biaya')
        }),
        ('Status & Tanggal', {
            'fields': ('rencana_tanggal_posting', 'tanggal_posting', 'is_posted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChannelPerformance)
class ChannelPerformanceAdmin(admin.ModelAdmin):
    list_display = ('channel', 'period', 'as_of_date', 'show_metrics', 'created_at')
    list_filter = ('period', 'as_of_date', 'channel__channel')
    search_fields = ('channel__judul',)
    ordering = ('-as_of_date', '-created_at')
    readonly_fields = ('created_at',)

    def show_metrics(self, obj):
        """Tampilkan metrik ringkas di admin list"""
        if not obj.metrics:
            return "-"
        preview = ", ".join(f"{k}: {v}" for k, v in obj.metrics.items())
        return preview[:80] + ("..." if len(preview) > 80 else "")
    show_metrics.short_description = "Metrics (Preview)"


from django.contrib import admin
from post_media.models.for_market import Market


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    name = ('name')
    description = ('description')