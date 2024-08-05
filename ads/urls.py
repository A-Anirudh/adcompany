from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', AdViewSet)

urlpatterns = [
    path('track-analytics/', TrackAnalyticsView.as_view(), name='track-analytics'),
    path('monthly-playtime/<int:ad_id>/', GetMonthlyPlaytimeView.as_view(), name='monthly-playtime'),
    path('all-monthly-playtime/<int:ad_id>/', GetAllMonthlyPlaytimeView.as_view(), name='get_all_monthly_playtime'),


    path('', include(router.urls)),
]