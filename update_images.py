import os
import django
from django.db import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lost_and_found.settings')
django.setup()

from core.models import LostItem, FoundItem

def update_images():
    print("Updating Lost Items...")
    lost_phone = LostItem.objects.filter(title__icontains='iPhone').first()
    if lost_phone:
        lost_phone.image = 'lost_items/phone.png'
        lost_phone.save()
        print(f"Updated {lost_phone.title}")

    lost_backpack = LostItem.objects.filter(title__icontains='Backpack').first()
    if lost_backpack:
        lost_backpack.image = 'lost_items/backpack.png'
        lost_backpack.save()
        print(f"Updated {lost_backpack.title}")

    print("Updating Found Items...")
    found_ring = FoundItem.objects.filter(title__icontains='Ring').first()
    if found_ring:
        found_ring.image = 'found_items/ring.png'
        found_ring.save()
        print(f"Updated {found_ring.title}")

if __name__ == '__main__':
    update_images()
