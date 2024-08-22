from django.urls import path
from .views import register_user, login_user, csrf_token_view, test_view, ad_preferences, logout_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_view, name='logout_user'),
    path('csrf-token/', csrf_token_view, name='csrf-token'),
    path('test/', test_view, name='test_view'),
    path('ad-preferences/', ad_preferences, name='ad-preferences-update'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh URL
]