from django.db import models
from django.utils import timezone

class Lead(models.Model):
    LEAD_SOURCE_CHOICES = [
        ('website', 'Website'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('referral', 'Referral'),
        ('fb_ads', 'FB Ads'),
        ('teknusa', 'Teknusa'),
        ('Self', 'Self'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('hot', 'Hot'),
        ('warm', 'Warm'),
        ('cold', 'Cold'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    account_medsos = models.CharField(max_length=200, blank=True, null=True, verbose_name="Account Medsos")
    lead_source = models.CharField(max_length=50, choices=LEAD_SOURCE_CHOICES, blank=True, null=True)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='warm')
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    next_follow_up = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.status})"

    @property
    def jumlah_interaksi(self):
        return self.interactions.count()

    @property
    def interaksi_terakhir(self):
        last = self.interactions.order_by('-created_at').first()
        return last.created_at if last else None

class Interaction(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interactions')
    note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Interaction with {self.lead.name} at {self.created_at:%Y-%m-%d}"
