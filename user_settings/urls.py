from django.urls import path
from . import views

app_name = 'user_settings'

urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-notifications/', views.update_notifications, name='update_notifications'),
    path('update-security/', views.update_security, name='update_security'),
    path('update-wallet/', views.update_wallet, name='update_wallet'),
]
