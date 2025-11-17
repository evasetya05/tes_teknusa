from django.contrib import admin
from .models import Idea, Build, Product, Measure, DataPoint, Learning

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('title', 'idea', 'status', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'build', 'public', 'created_at')

@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ('metric', 'product', 'current', 'target')

@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ('measure', 'value', 'measured_at')

@admin.register(Learning)
class LearningAdmin(admin.ModelAdmin):
    list_display = ('summary', 'idea', 'created_at')