from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from ownership.models import Transaction, Property, Area
from django.db.models import Count, Sum

def ownership_view(request):
    # Get all transactions ordered by creation date (newest first)
    all_transactions = Transaction.objects.select_related('customer', 'property__area').order_by('-created_at')

    # Paginate - show 8 transactions per page to fit nicely
    paginator = Paginator(all_transactions, 8)
    page_number = request.GET.get('page', 1)
    transactions = paginator.get_page(page_number)

    # Get area statistics for pie chart
    area_stats = Property.objects.values('area__name').annotate(
        property_count=Count('id')
    ).order_by('-property_count')

    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for AJAX pagination
        transactions_html = render_to_string('ownership/partials/transactions_table.html', {
            'transactions': transactions
        })

        return JsonResponse({
            'transactions_html': transactions_html,
            'has_previous': transactions.has_previous(),
            'has_next': transactions.has_next(),
            'previous_page_number': transactions.previous_page_number() if transactions.has_previous() else None,
            'next_page_number': transactions.next_page_number() if transactions.has_next() else None,
            'current_page': transactions.number,
            'total_pages': transactions.paginator.num_pages,
        })

    context = {
        'transactions': transactions,
        'area_stats': list(area_stats)
    }

    return render(request, 'ownership/ownership.html', context)
