from django.shortcuts import render
from ownership.models import Transaction  # if you've defined this model

def ownership_view(request):
    transactions = Transaction.objects.select_related('customer', 'property__area').all()
    return render(request, 'ownership/ownership.html', {'transactions': transactions})
