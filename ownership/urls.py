from django.urls import path
from . import views

urlpatterns = [
    path('', views.ownership_view, name='ownership_home'),
]
