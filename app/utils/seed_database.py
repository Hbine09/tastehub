from app import db
from datetime import datetime

def seed_menu_items():
    """Add sample menu items to Firestore"""
    
    menu_items = [
        {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza with fresh mozzarella, tomatoes, and basil',
            'price': 12.99,
            'category': 'Pizza',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Pepperoni Pizza',
            'description': 'Traditional pizza topped with pepperoni and cheese',
            'price': 14.99,
            'category': 'Pizza',
            'image_url': None,
            'available': True
        },
        {
            'name': 'BBQ Chicken Pizza',
            'description': 'Grilled chicken with BBQ sauce, red onions, and cilantro',
            'price': 15.99,
            'category': 'Pizza',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Caesar Salad',
            'description': 'Crisp romaine lettuce with Caesar dressing and croutons',
            'price': 8.99,
            'category': 'Salads',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Greek Salad',
            'description': 'Fresh vegetables with feta cheese and olives',
            'price': 9.99,
            'category': 'Salads',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Chicken Wings',
            'description': 'Crispy wings with your choice of sauce',
            'price': 10.99,
            'category': 'Appetizers',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Mozzarella Sticks',
            'description': 'Breaded mozzarella served with marinara sauce',
            'price': 7.99,
            'category': 'Appetizers',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Garlic Bread',
            'description': 'Toasted bread with garlic butter and herbs',
            'price': 5.99,
            'category': 'Appetizers',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Chocolate Lava Cake',
            'description': 'Warm chocolate cake with molten center',
            'price': 6.99,
            'category': 'Desserts',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Tiramisu',
            'description': 'Classic Italian dessert with coffee and mascarpone',
            'price': 7.99,
            'category': 'Desserts',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Coca Cola',
            'description': 'Chilled soft drink',
            'price': 2.99,
            'category': 'Beverages',
            'image_url': None,
            'available': True
        },
        {
            'name': 'Iced Tea',
            'description': 'Freshly brewed iced tea',
            'price': 2.49,
            'category': 'Beverages',
            'image_url': None,
            'available': True
        }
    ]
    
    menu_ref = db.collection('menu_items')
    
    # Clear existing items (optional - remove if you want to keep existing data)
    existing_docs = menu_ref.stream()
    for doc in existing_docs:
        doc.reference.delete()
    
    # Add new items
    added_count = 0
    for item in menu_items:
        item['created_at'] = datetime.utcnow()
        item['updated_at'] = datetime.utcnow()
        menu_ref.add(item)
        added_count += 1
        print(f"Added: {item['name']}")
    
    print(f"\n✅ Successfully added {added_count} menu items!")
    return added_count

def seed_sample_order():
    """Add a sample order for testing"""
    
    sample_order = {
        'user_id': 'sample_user',
        'user_name': 'Test User',
        'user_email': 'test@example.com',
        'items': [
            {
                'name': 'Margherita Pizza',
                'price': 12.99,
                'quantity': 2
            },
            {
                'name': 'Caesar Salad',
                'price': 8.99,
                'quantity': 1
            }
        ],
        'total': 34.97,
        'status': 'delivered',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    orders_ref = db.collection('orders')
    orders_ref.add(sample_order)
    print("✅ Sample order added!")

if __name__ == '__main__':
    print("Starting data seeding...")
    seed_menu_items()
    seed_sample_order()
    print("\n🎉 Data seeding complete!")