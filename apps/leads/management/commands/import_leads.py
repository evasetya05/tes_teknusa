from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from leads.models import Lead

class Command(BaseCommand):
    help = 'Import leads from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        status_mapping = {
            'converted': 'won',
            'new': 'new',
            'contacted': 'contacted',
            'qualified': 'qualified',
            'lost': 'lost',
        }

        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Map old status to new
                status = status_mapping.get(row['status'], 'new')

                # Check if lead already exists
                if Lead.objects.filter(name=row['name']).exists():
                    self.stdout.write(f"Skipping existing lead: {row['name']}")
                    continue
                created_at = None
                if row['created_at']:
                    try:
                        created_at = datetime.fromisoformat(row['created_at'])
                    except ValueError:
                        self.stdout.write(f"Invalid created_at for {row['name']}: {row['created_at']}")

                # Create Lead
                lead = Lead(
                    name=row['name'],
                    email=row.get('email') or None,
                    phone=row.get('phone') or None,
                    company=row.get('company') or None,
                    account_medsos=None,  # Not in CSV, set to None
                    status=status,
                    created_at=created_at,
                    # Set defaults for new fields
                    lead_source=None,
                    assigned_to=None,
                    priority='warm',
                    estimated_value=None,
                    next_follow_up=None,
                )
                lead.pk = int(row['id'])  # Set pk to preserve ids
                lead.save()
                self.stdout.write(f"Imported lead: {lead.name} (id: {lead.pk})")

        self.stdout.write('Import completed.')
