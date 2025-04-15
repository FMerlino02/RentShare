from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ownership.models import Area

@login_required
def index(request):
    areas = Area.objects.prefetch_related('properties').all()
    return render(request, 'dashboard/dashboard.html', {'areas': areas})
