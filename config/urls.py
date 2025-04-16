from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from django.conf.urls.static import static
from django.conf import settings
from dashboard.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('contracts/', include('contracts.urls')),
    path('ownership/', include('ownership.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)