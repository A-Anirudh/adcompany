from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Includes user-related URLs
    path('api/ads/', include('ads.urls')),  # Includes ad-related URLs
]
