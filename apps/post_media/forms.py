from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Channel, ChannelPerformance

class ChannelForm(forms.ModelForm):
    isi_konten = forms.CharField(
        label="Isi Konten",
        widget=CKEditorUploadingWidget()
    )

    rencana_tanggal_posting = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        )
    )

    tanggal_posting = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Channel
        fields = [
            'akun',
            'for_market',
            'channel',
            'funnel_stage',
            'kategori_biaya',
            'rencana_tanggal_posting',
            'tanggal_posting',
            'is_posted',
            'jenis_konten',
            'judul',
            'isi_konten',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # format data awal agar sesuai dengan HTML5
        if self.instance and self.instance.pk:
            if self.instance.tanggal_posting:
                self.initial['tanggal_posting'] = self.instance.tanggal_posting.strftime('%Y-%m-%dT%H:%M')
            if self.instance.rencana_tanggal_posting:
                self.initial['rencana_tanggal_posting'] = self.instance.rencana_tanggal_posting.strftime('%Y-%m-%d')


# ---- Form untuk update performance ----
class ChannelPerformanceForm(forms.ModelForm):
    class Meta:
        model = ChannelPerformance
        fields = ['period', 'metrics']
