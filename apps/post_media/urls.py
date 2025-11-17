# post_media/urls.py
from django.urls import path
from post_media.views.post_media_home import post_media_home
from post_media.views.channel import channel_list, channel_detail, channel_add, channel_edit, channel_analytics, update_performance, export_channel_analytics_excel

app_name = 'post_media'

urlpatterns = [
    path('post_media_home/', post_media_home, name='post_media_home'),
    path('', channel_list, name='channel_list'),
    path('channel/<int:pk>/', channel_detail, name='channel_detail'),
    path('add/', channel_add, name='channel_add'),
    path('edit/<int:pk>/', channel_edit, name='channel_edit'),
    path('analytics/', channel_analytics, name='channel_analytics'),
    path('analytics/export/', export_channel_analytics_excel, name='export_channel_analytics_excel'),
    path('channel/<int:pk>/update-performance/', update_performance, name='update_performance'),

    
]
