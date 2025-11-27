from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ownership.models import Property, Transaction, Investment, Certificate
from decimal import Decimal
import requests
import hashlib
import uuid
from datetime import datetime

def get_btc_price():
    """Fetch current BTC/USD price from CoinGecko API"""
    try:
        response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price',
            params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return Decimal(str(data['bitcoin']['usd']))
    except:
        pass
    # Fallback price if API fails
    return Decimal('45000.00')

@login_required
def marketplace_view(request):
    # Get all properties with available shares
    properties = Property.objects.select_related('area', 'owner').all().order_by('-created_at')

    # Get current BTC price
    btc_price = get_btc_price()

    # Calculate available shares and prices for each property
    property_listings = []
    for prop in properties:
        available_shares = prop.total_shares - prop.shares_sold
        price_usd = prop.price_per_share
        price_btc = price_usd / btc_price if btc_price > 0 else Decimal('0')

        property_listings.append({
            'property': prop,
            'available_shares': available_shares,
            'price_usd': price_usd,
            'price_btc': price_btc,
            'total_value_usd': price_usd * prop.total_shares,
        })

    context = {
        'properties': property_listings,
        'btc_price': btc_price,
    }

    return render(request, 'marketplace/marketplace.html', context)

@login_required
@require_POST
def purchase_shares(request):
    """Handle share purchase requests"""
    try:
        property_id = request.POST.get('property_id')
        shares_amount = int(request.POST.get('shares_amount', 0))
        wallet_address = request.POST.get('wallet_address')
        payment_method = request.POST.get('payment_method')  # 'metamask' or 'phantom'

        if shares_amount <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid share amount'})

        # Get property
        prop = get_object_or_404(Property, id=property_id)

        # Check if enough shares available
        available_shares = prop.total_shares - prop.shares_sold
        if shares_amount > available_shares:
            return JsonResponse({'success': False, 'error': f'Only {available_shares} shares available'})

        # Calculate price
        total_price = prop.price_per_share * shares_amount

        # Create transaction
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        transaction = Transaction.objects.create(
            order_id=order_id,
            customer=request.user,
            property=prop,
            shares_amount=shares_amount,
            price=total_price,
            status='processing'
        )

        # Update shares sold
        prop.shares_sold += shares_amount
        prop.save()

        # Create or update investment
        investment, created = Investment.objects.get_or_create(
            user=request.user,
            property=prop,
            defaults={'share_count': shares_amount}
        )
        if not created:
            investment.share_count += shares_amount
            investment.save()

        # Create certificate
        certificate_data = f"{request.user.id}-{prop.id}-{shares_amount}-{datetime.now().isoformat()}"
        certificate_hash = hashlib.sha256(certificate_data.encode()).hexdigest()

        Certificate.objects.create(
            user=request.user,
            property=prop,
            share_count=shares_amount,
            certificate_hash=certificate_hash
        )

        return JsonResponse({
            'success': True,
            'order_id': order_id,
            'message': f'Successfully purchased {shares_amount} shares!',
            'wallet': wallet_address,
            'payment_method': payment_method
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
