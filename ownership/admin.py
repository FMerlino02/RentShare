from django.contrib import admin
from .models import Property, Transaction, Investment, Certificate

admin.site.register(Property)
admin.site.register(Transaction)
admin.site.register(Investment)
admin.site.register(Certificate)
