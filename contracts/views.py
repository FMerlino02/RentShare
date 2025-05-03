from django.shortcuts import render

def contracts_view(request):
    return render(request, 'contracts/contracts.html')