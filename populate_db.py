import os
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from ownership.models import Area, Property

def download_image(url, filename):
    """Download an image from URL and return a ContentFile"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content, name=filename)
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

def populate_database():
    print("Starting database population...")

    # Get or create the admin user
    admin_user = User.objects.get(username='admin')
    print(f"Using user: {admin_user.username}")

    # Create areas
    areas_data = [
        'Downtown',
        'Suburbs',
        'Waterfront',
        'Historic District',
        'Business District'
    ]

    areas = []
    for area_name in areas_data:
        area, created = Area.objects.get_or_create(name=area_name)
        areas.append(area)
        print(f"{'Created' if created else 'Found'} area: {area_name}")

    # Property data with Unsplash image URLs (architecture/houses)
    properties_data = [
        {
            'name': 'Sunset Villa',
            'location': 'Beverly Hills, CA',
            'lat': 34.0736,
            'lng': -118.4004,
            'total_shares': 1000,
            'shares_sold': 450,
            'area': areas[0],
            'image_url': 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=80'
        },
        {
            'name': 'Ocean View Apartment',
            'location': 'Miami Beach, FL',
            'lat': 25.7907,
            'lng': -80.1300,
            'total_shares': 800,
            'shares_sold': 320,
            'area': areas[2],
            'image_url': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80'
        },
        {
            'name': 'Modern Loft',
            'location': 'New York, NY',
            'lat': 40.7128,
            'lng': -74.0060,
            'total_shares': 1200,
            'shares_sold': 890,
            'area': areas[4],
            'image_url': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80'
        },
        {
            'name': 'Garden Estate',
            'location': 'Portland, OR',
            'lat': 45.5152,
            'lng': -122.6784,
            'total_shares': 500,
            'shares_sold': 125,
            'area': areas[1],
            'image_url': 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&q=80'
        },
        {
            'name': 'Victorian Manor',
            'location': 'San Francisco, CA',
            'lat': 37.7749,
            'lng': -122.4194,
            'total_shares': 1500,
            'shares_sold': 1100,
            'area': areas[3],
            'image_url': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=80'
        },
        {
            'name': 'Lakeside Cottage',
            'location': 'Seattle, WA',
            'lat': 47.6062,
            'lng': -122.3321,
            'total_shares': 600,
            'shares_sold': 280,
            'area': areas[2],
            'image_url': 'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=800&q=80'
        },
        {
            'name': 'Downtown Penthouse',
            'location': 'Chicago, IL',
            'lat': 41.8781,
            'lng': -87.6298,
            'total_shares': 2000,
            'shares_sold': 1450,
            'area': areas[0],
            'image_url': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80'
        },
        {
            'name': 'Suburban Family Home',
            'location': 'Austin, TX',
            'lat': 30.2672,
            'lng': -97.7431,
            'total_shares': 700,
            'shares_sold': 350,
            'area': areas[1],
            'image_url': 'https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?w=800&q=80'
        },
        {
            'name': 'Historic Townhouse',
            'location': 'Boston, MA',
            'lat': 42.3601,
            'lng': -71.0589,
            'total_shares': 900,
            'shares_sold': 540,
            'area': areas[3],
            'image_url': 'https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800&q=80'
        },
        {
            'name': 'Beachfront Condo',
            'location': 'San Diego, CA',
            'lat': 32.7157,
            'lng': -117.1611,
            'total_shares': 1100,
            'shares_sold': 775,
            'area': areas[2],
            'image_url': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80'
        }
    ]

    # Create properties
    created_count = 0
    for prop_data in properties_data:
        # Check if property already exists
        if Property.objects.filter(property_name=prop_data['name']).exists():
            print(f"Property '{prop_data['name']}' already exists, skipping...")
            continue

        print(f"Creating property: {prop_data['name']}...")

        # Download image
        image_file = download_image(
            prop_data['image_url'],
            f"{prop_data['name'].lower().replace(' ', '_')}.jpg"
        )

        if image_file:
            # Create property
            property_obj = Property.objects.create(
                owner=admin_user,
                area=prop_data['area'],
                property_name=prop_data['name'],
                location=prop_data['location'],
                latitude=prop_data['lat'],
                longitude=prop_data['lng'],
                total_shares=prop_data['total_shares'],
                shares_sold=prop_data['shares_sold'],
                image=image_file
            )
            created_count += 1
            print(f"[OK] Created: {prop_data['name']}")
        else:
            print(f"[FAILED] Failed to create {prop_data['name']} - image download failed")

    print(f"\nDatabase population complete!")
    print(f"Total properties created: {created_count}")
    print(f"Total properties in database: {Property.objects.count()}")
    print(f"Total areas: {Area.objects.count()}")

if __name__ == '__main__':
    populate_database()
