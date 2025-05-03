from django.urls import path
from . import views

urlpatterns = [
    path('', views.contracts_view, name='contracts')
]
