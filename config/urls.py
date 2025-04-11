from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('contracts/', include('contracts.urls')),
    path('ownership/', include('ownership.urls')),
]
