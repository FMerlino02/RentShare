from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='properties')
    property_name = models.CharField(max_length=150)
    location = models.CharField(max_length=255, null=True, blank=True)
    total_shares = models.PositiveIntegerField()
    shares_sold = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property_name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    real_property = models.ForeignKey(Property, on_delete=models.RESTRICT)
    shares_purchased = models.PositiveIntegerField()
    share_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_amount(self):
        return self.shares_purchased * self.share_price

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    property = models.ForeignKey(Property, on_delete=models.RESTRICT)
    share_count = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    property = models.ForeignKey(Property, on_delete=models.RESTRICT)
    share_count = models.PositiveIntegerField()
    certificate_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
