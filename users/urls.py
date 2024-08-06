from django.urls import path
from .views import register_user, login_user, csrf_token_view

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('api/csrf-token/', csrf_token_view, name='csrf-token'),
]
