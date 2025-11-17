from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix datetime fields that are stored as strings using raw SQL'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Fix Lead created_at
            cursor.execute("""
                UPDATE leads_lead
                SET created_at = STR_TO_DATE(created_at, '%Y-%m-%d %H:%i:%s')
                WHERE created_at REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'
            """)
            self.stdout.write(f'Updated {cursor.rowcount} leads created_at')

            # Fix Interaction created_at
            cursor.execute("""
                UPDATE leads_interaction
                SET created_at = STR_TO_DATE(created_at, '%Y-%m-%d %H:%i:%s')
                WHERE created_at REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'
            """)
            self.stdout.write(f'Updated {cursor.rowcount} interactions created_at')

        self.stdout.write('Datetime fields fixed.')
