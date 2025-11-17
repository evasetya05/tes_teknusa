# portfolio/admin.py

from django.contrib import admin
from .models import Portfolio

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'views', 'created_at')
    search_fields = ('title', 'about')
    list_filter = ('status', 'created_at')
