from django.core.management.base import BaseCommand
from django.utils import timezone
from leads.models import Lead, Interaction
from dateutil import parser

class Command(BaseCommand):
    help = 'Fix datetime fields that are stored as strings'

    def handle(self, *args, **options):
        # Fix Lead created_at
        for lead in Lead.objects.all():
            if isinstance(lead.created_at, str):
                try:
                    lead.created_at = parser.parse(lead.created_at)
                    lead.save(update_fields=['created_at'])
                    self.stdout.write(f'Fixed created_at for lead {lead.pk}')
                except Exception as e:
                    self.stdout.write(f'Error fixing lead {lead.pk}: {e}')

        # Fix Interaction created_at
        for interaction in Interaction.objects.all():
            if isinstance(interaction.created_at, str):
                try:
                    interaction.created_at = parser.parse(interaction.created_at)
                    interaction.save(update_fields=['created_at'])
                    self.stdout.write(f'Fixed created_at for interaction {interaction.pk}')
                except Exception as e:
                    self.stdout.write(f'Error fixing interaction {interaction.pk}: {e}')

        self.stdout.write('Datetime fields fixed.')
