from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def settings_view(request):
    """Main settings page with tabbed sections"""
    context = {
        'user': request.user,
    }
    return render(request, 'user_settings/settings.html', context)

@login_required
@require_POST
def update_profile(request):
    """Handle profile updates (MVP - simulated)"""
    # In a real app, this would update the user model
    return JsonResponse({'success': True, 'message': 'Profile updated successfully!'})

@login_required
@require_POST
def update_notifications(request):
    """Handle notification preferences (MVP - simulated)"""
    return JsonResponse({'success': True, 'message': 'Notification preferences saved!'})

@login_required
@require_POST
def update_security(request):
    """Handle security settings (MVP - simulated)"""
    return JsonResponse({'success': True, 'message': 'Security settings updated!'})

@login_required
@require_POST
def update_wallet(request):
    """Handle wallet preferences (MVP - simulated)"""
    return JsonResponse({'success': True, 'message': 'Wallet settings saved!'})
