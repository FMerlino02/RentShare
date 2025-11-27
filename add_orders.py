import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from ownership.models import Property, Transaction, Investment, Certificate
import hashlib

def generate_order_id():
    """Generate a unique order ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = random.randint(1000, 9999)
    return f"ORD{timestamp[-8:]}{random_part}"

def generate_certificate_hash(user, property_obj, share_count):
    """Generate a certificate hash"""
    data = f"{user.id}{property_obj.id}{share_count}{datetime.now()}"
    return hashlib.sha256(data.encode()).hexdigest()

def create_orders():
    print("Creating mock orders and transactions...")

    # Get admin user
    admin_user = User.objects.get(username='admin')

    # Create some additional users for transactions
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'bob_johnson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
        {'username': 'alice_williams', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Williams'},
        {'username': 'charlie_brown', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
    ]

    users = [admin_user]
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user_data['username']}")
        else:
            print(f"Found user: {user_data['username']}")
        users.append(user)

    # Get all properties
    properties = list(Property.objects.all())

    if not properties:
        print("No properties found! Please run populate_db.py first.")
        return

    # Create transactions
    statuses = ['processing', 'accepted', 'declined']
    transactions_created = 0
    investments_created = 0
    certificates_created = 0

    # Create 20-30 transactions
    num_transactions = random.randint(20, 30)

    for i in range(num_transactions):
        # Random user and property
        user = random.choice(users)
        property_obj = random.choice(properties)

        # Random shares (1-50)
        shares = random.randint(1, 50)

        # Random price per share ($100-$1000)
        price_per_share = random.uniform(100, 1000)
        total_price = round(shares * price_per_share, 2)

        # Random status (80% accepted, 10% processing, 10% declined)
        rand = random.random()
        if rand < 0.8:
            status = 'accepted'
        elif rand < 0.9:
            status = 'processing'
        else:
            status = 'declined'

        # Check if order already exists
        order_id = generate_order_id()
        while Transaction.objects.filter(order_id=order_id).exists():
            order_id = generate_order_id()

        # Create transaction
        transaction = Transaction.objects.create(
            order_id=order_id,
            customer=user,
            property=property_obj,
            shares_amount=shares,
            price=total_price,
            status=status
        )

        # Set created_at to a random date in the past 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        transaction.created_at = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        transaction.save()

        transactions_created += 1
        print(f"[OK] Created transaction {order_id}: {user.username} bought {shares} shares of {property_obj.property_name} for ${total_price} ({status})")

        # If accepted, create investment and certificate
        if status == 'accepted':
            # Create or update investment
            investment, created = Investment.objects.get_or_create(
                user=user,
                property=property_obj,
                defaults={'share_count': shares}
            )

            if not created:
                investment.share_count += shares
                investment.save()
                print(f"  [+] Updated investment: {user.username} now has {investment.share_count} shares")
            else:
                investments_created += 1
                print(f"  [+] Created investment: {user.username} has {shares} shares")

            # Create certificate
            cert_hash = generate_certificate_hash(user, property_obj, shares)
            certificate = Certificate.objects.create(
                user=user,
                property=property_obj,
                share_count=shares,
                certificate_hash=cert_hash
            )
            certificate.created_at = transaction.created_at
            certificate.save()
            certificates_created += 1
            print(f"  [+] Created certificate with hash: {cert_hash[:16]}...")

    print(f"\n{'='*60}")
    print(f"Order creation complete!")
    print(f"{'='*60}")
    print(f"Users created/found: {len(users)}")
    print(f"Transactions created: {transactions_created}")
    print(f"  - Accepted: {Transaction.objects.filter(status='accepted').count()}")
    print(f"  - Processing: {Transaction.objects.filter(status='processing').count()}")
    print(f"  - Declined: {Transaction.objects.filter(status='declined').count()}")
    print(f"Investments created/updated: {investments_created}")
    print(f"Certificates created: {certificates_created}")
    print(f"\nTotal transactions in database: {Transaction.objects.count()}")
    print(f"Total investments in database: {Investment.objects.count()}")
    print(f"Total certificates in database: {Certificate.objects.count()}")

if __name__ == '__main__':
    create_orders()
