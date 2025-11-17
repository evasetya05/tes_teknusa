from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('lead/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('create/', views.lead_create, name='lead_create'),
    path('lead/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('analysis/', views.lead_analysis, name='lead_analysis'),
    path('graphic/', views.lead_graphic, name='lead_graphic'),
]
