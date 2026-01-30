import unittest
from app.models.user import User
from app.models.menu_item import MenuItem
from datetime import datetime


class TestUserModel(unittest.TestCase):
    """Test cases for User model"""
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User(
            uid='test123',
            email='test@example.com',
            name='Test User',
            role='customer'
        )
        
        self.assertEqual(user.uid, 'test123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.role, 'customer')
    
    def test_user_to_dict(self):
        """Test converting user to dictionary"""
        user = User(
            uid='test123',
            email='test@example.com',
            name='Test User',
            role='customer'
        )
        
        user_dict = user.to_dict()
        
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['uid'], 'test123')
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertIn('created_at', user_dict)
    
    def test_user_from_dict(self):
        """Test creating user from dictionary"""
        data = {
            'uid': 'test456',
            'email': 'user@test.com',
            'name': 'Another User',
            'role': 'staff'
        }
        
        user = User.from_dict(data)
        
        self.assertEqual(user.uid, 'test456')
        self.assertEqual(user.email, 'user@test.com')
        self.assertEqual(user.role, 'staff')
    
    def test_default_role(self):
        """Test that default role is customer"""
        user = User(
            uid='test789',
            email='default@example.com',
            name='Default User'
        )
        
        self.assertEqual(user.role, 'customer')


class TestMenuItemModel(unittest.TestCase):
    """Test cases for MenuItem model"""
    
    def test_menu_item_creation(self):
        """Test creating a menu item"""
        item = MenuItem(
            item_id='item123',
            name='Test Pizza',
            description='A test pizza',
            price=15.99,
            category='Pizza',
            available=True
        )
        
        self.assertEqual(item.item_id, 'item123')
        self.assertEqual(item.name, 'Test Pizza')
        self.assertEqual(item.price, 15.99)
        self.assertEqual(item.category, 'Pizza')
        self.assertTrue(item.available)
    
    def test_menu_item_to_dict(self):
        """Test converting menu item to dictionary"""
        item = MenuItem(
            item_id='item456',
            name='Caesar Salad',
            description='Fresh salad',
            price=9.99,
            category='Salads'
        )
        
        item_dict = item.to_dict()
        
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['name'], 'Caesar Salad')
        self.assertEqual(item_dict['price'], 9.99)
        self.assertIn('available', item_dict)
    
    def test_menu_item_from_dict(self):
        """Test creating menu item from dictionary"""
        data = {
            'item_id': 'item789',
            'name': 'Garlic Bread',
            'description': 'Toasted bread',
            'price': 5.99,
            'category': 'Appetizers',
            'available': False
        }
        
        item = MenuItem.from_dict(data)
        
        self.assertEqual(item.name, 'Garlic Bread')
        self.assertEqual(item.price, 5.99)
        self.assertFalse(item.available)
    
    def test_default_availability(self):
        """Test that items are available by default"""
        item = MenuItem(
            item_id='item999',
            name='Default Item',
            description='Test',
            price=10.00,
            category='Test'
        )
        
        self.assertTrue(item.available)


if __name__ == '__main__':
    unittest.main()