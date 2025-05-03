from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from ownership.models import Property, Area
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.shortcuts import redirect, get_object_or_404

@login_required
def index(request):
    areas = Area.objects.prefetch_related('properties').all()
    return render(request, 'dashboard/dashboard.html', {'areas': areas})

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

@login_required
def add_property(request):
    if request.method == "POST":
        property_name = request.POST.get("property_name")
        location = request.POST.get("location")
        total_shares = request.POST.get("total_shares")
        shares_sold = request.POST.get("shares_sold")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        area_id = request.POST.get("area")
        image = request.FILES.get("image")

        Property.objects.create(
            property_name=property_name,
            location=location,
            total_shares=total_shares,
            shares_sold=0,
            latitude=latitude,
            longitude=longitude,
            area_id=area_id,
            image=image,
            owner=request.user,
        )
    return redirect('dashboard')

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == "POST":
        property.delete()
    return redirect('dashboard')  # Make sure this is your dashboard view name