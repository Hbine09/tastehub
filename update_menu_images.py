import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import db

# Free food images from Unsplash
menu_images = {
    'Margherita Pizza': 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500',
    'Pepperoni Pizza': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500',
    'BBQ Chicken Pizza': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500',
    'Caesar Salad': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=500',
    'Greek Salad': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500',
    'Chicken Wings': 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=500',
    'Mozzarella Sticks': 'https://images.unsplash.com/photo-1531749668029-2db88e4276c7?w=500',
    'Garlic Bread': 'https://images.unsplash.com/photo-1573140401552-388e2e4c4723?w=500',
    'Chocolate Lava Cake': 'https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=500',
    'Tiramisu': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500',
    'Coca Cola': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=500',
    'Iced Tea': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500'
}

def update_images():
    """Update menu items with image URLs"""
    menu_ref = db.collection('menu_items')
    
    updated_count = 0
    docs = menu_ref.stream()
    
    for doc in docs:
        item_data = doc.to_dict()
        item_name = item_data.get('name')
        
        if item_name in menu_images:
            doc.reference.update({
                'image_url': menu_images[item_name]
            })
            print(f"✅ Updated image for: {item_name}")
            updated_count += 1
        else:
            print(f"⚠️  No image found for: {item_name}")
    
    print(f"\n🎉 Updated {updated_count} menu items with images!")

if __name__ == '__main__':
    print("Updating menu item images...")
    print("=" * 50)
    update_images()