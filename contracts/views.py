from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ownership.models import Investment, Certificate
from decimal import Decimal

@login_required
def contracts_view(request):
    # Get user's investments with related property and area data
    user_investments = Investment.objects.filter(
        user=request.user
    ).select_related('property', 'property__area').order_by('-share_count')

    # Calculate investment details for each property
    investment_details = []
    total_monthly_return = Decimal('0.00')

    for investment in user_investments:
        # Calculate share percentage
        if investment.property.total_shares > 0:
            share_percentage = (investment.share_count / investment.property.total_shares) * 100
        else:
            share_percentage = 0

        # Calculate monthly return (mock calculation: $5-15 per share)
        monthly_return = Decimal(str(investment.share_count)) * Decimal('7.50')
        total_monthly_return += monthly_return

        # Get certificate for this investment
        certificate = Certificate.objects.filter(
            user=request.user,
            property=investment.property
        ).first()

        investment_details.append({
            'investment': investment,
            'share_percentage': round(share_percentage, 2),
            'monthly_return': monthly_return,
            'certificate': certificate,
            'certificate_id': certificate.id if certificate else None
        })

    context = {
        'investments': investment_details,
        'total_monthly_return': total_monthly_return,
        'has_investments': len(investment_details) > 0
    }

    return render(request, 'contracts/contracts.html', context)