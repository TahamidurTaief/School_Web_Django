from django.urls import path
from .views import notice_list, filter_notices, download_notice

urlpatterns = [
    path('notices/', notice_list, name='notice_list'),
    path('filter-notices/', filter_notices, name='filter_notices'),
    path('download-notice/<int:pk>/', download_notice, name='download_notice'),
]