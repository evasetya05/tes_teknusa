from django.urls import path
from .apiview import (
    LikeListAPIView,
    UserCountOfLikesAPIView,
    LikeToggleView,
    IsLikedAPIView,
)

app_name = 'likes-api'

urlpatterns = [
    path('likes/list/', LikeListAPIView.as_view(), name='list'),
    path('likes/count/', UserCountOfLikesAPIView.as_view(), name='count'),
    path('likes/toggle/', LikeToggleView.as_view(), name='toggle'),
    path('likes/is/', IsLikedAPIView.as_view(), name='is'),
]
