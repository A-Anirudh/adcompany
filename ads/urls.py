from django.urls import path
from .views import ad_operations, track_analytics, get_monthly_playtime, get_all_monthly_playtime

urlpatterns = [
    path('', ad_operations, name='ad-list-create'),
    path('<int:ad_id>/', ad_operations, name='ad-retrieve-update-delete'),
    path('track-analytics/', track_analytics, name='track-analytics'),
    path('monthly-playtime/<int:ad_id>/', get_monthly_playtime, name='monthly-playtime'),
    path('all-monthly-playtime/<int:ad_id>/', get_all_monthly_playtime, name='get_all_monthly_playtime'),
]
