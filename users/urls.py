from django.urls import path
from .views import register_user, login_user, csrf_token_view,test_view,update_ad_preferences

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('api/csrf-token/', csrf_token_view, name='csrf-token'),
    path('test/', test_view, name='test_view'),
    path('ad-preferences/', update_ad_preferences, name='ad-preferences-update'),
]