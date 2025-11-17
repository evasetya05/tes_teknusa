from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from leads.models import Interaction, Lead

class Command(BaseCommand):
    help = 'Import interactions from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get the lead
                try:
                    lead = Lead.objects.get(pk=int(row['lead_id']))
                except Lead.DoesNotExist:
                    self.stdout.write(f"Lead with id {row['lead_id']} not found, skipping interaction {row['id']}")
                    continue

                # Parse created_at
                created_at = None
                if row['created_at']:
                    try:
                        created_at = datetime.fromisoformat(row['created_at'])
                    except ValueError:
                        self.stdout.write(f"Invalid created_at for interaction {row['id']}: {row['created_at']}")

                # Create Interaction
                interaction = Interaction(
                    lead=lead,
                    note=row['note'],
                    created_at=created_at,
                )
                interaction.pk = int(row['id'])  # Set pk to preserve ids
                interaction.save()
                self.stdout.write(f"Imported interaction for {lead.name}")

        self.stdout.write('Import completed.')
