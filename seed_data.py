import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lost_and_found.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import LostItem, FoundItem

def seed_data():
    # Create a test user if not exists
    user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        user.set_password('password123')
        user.save()
        print(f"Created user: {user.username}")
    else:
        print(f"User {user.username} already exists")

    # Create Lost Items
    if not LostItem.objects.exists():
        LostItem.objects.create(
            title='Lost iPhone 13',
            description='Black iPhone 13 in a clear case. Lost near the cafeteria.',
            category='Electronics',
            location_lost='Cafeteria',
            date_lost=timezone.now().date(),
            reported_by=user,
            status='OPEN'
        )
        LostItem.objects.create(
            title='Blue Backpack',
            description='Nike backpack with textbooks inside.',
            category='Other',
            location_lost='Library',
            date_lost=timezone.now().date(),
            reported_by=user,
            status='OPEN'
        )
        print("Created sample Lost Items")
    else:
        print("Lost Items already exist")

    # Create Found Items
    if not FoundItem.objects.exists():
        FoundItem.objects.create(
            title='Gold Ring',
            description='Gold wedding band found in the parking lot.',
            category='Jewelry',
            location_found='Parking Lot B',
            date_found=timezone.now().date(),
            found_by=user
        )
        print("Created sample Found Items")
    else:
        print("Found Items already exist")

if __name__ == '__main__':
    seed_data()
