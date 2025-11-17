from django.urls import path
from . import views

app_name = 'lean'

urlpatterns = [
    path('', views.IdeaListView.as_view(), name='idea_list'),
    path('ideas/create/', views.idea_create, name='idea_create'),
    path('idea/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('idea/<int:pk>/edit/', views.idea_edit, name='idea_edit'),
    path('build/<int:pk>/edit/', views.build_edit, name='build_edit'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('measure/<int:pk>/edit/', views.measure_edit, name='measure_edit'),
    path('datapoint/<int:pk>/edit/', views.datapoint_edit, name='datapoint_edit'),
    path('learning/<int:pk>/edit/', views.learning_edit, name='learning_edit'),
]
