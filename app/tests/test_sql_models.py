import unittest
from app.models.sql_models import SQLOrder, SQLOrderItem


class TestSQLModels(unittest.TestCase):
    """Test cases for SQL models"""
    
    def test_order_creation(self):
        """Test creating an order object"""
        order = SQLOrder(
            user_id='user123',
            user_name='Test User',
            user_email='test@example.com',
            total=25.99,
            status='pending'
        )
        
        self.assertEqual(order.user_id, 'user123')
        self.assertEqual(order.user_name, 'Test User')
        self.assertEqual(order.total, 25.99)
        self.assertEqual(order.status, 'pending')
    
    def test_order_item_creation(self):
        """Test creating an order item object"""
        item = SQLOrderItem(
            order_id=1,
            item_name='Pizza',
            item_price=12.99,
            quantity=2
        )
        
        self.assertEqual(item.order_id, 1)
        self.assertEqual(item.item_name, 'Pizza')
        self.assertEqual(item.item_price, 12.99)
        self.assertEqual(item.quantity, 2)
    
    def test_order_to_dict(self):
        """Test converting order to dictionary"""
        order = SQLOrder(
            user_id='user456',
            user_name='Another User',
            user_email='user@test.com',
            total=50.00,
            status='completed'
        )
        
        # Manually set order_items to empty list for testing
        order.order_items = []
        order_dict = order.to_dict()
        
        self.assertIsInstance(order_dict, dict)
        self.assertEqual(order_dict['user_id'], 'user456')
        self.assertEqual(order_dict['total'], 50.00)
        self.assertIn('items', order_dict)
        self.assertIsInstance(order_dict['items'], list)
    
    def test_order_item_to_dict(self):
        """Test converting order item to dictionary"""
        item = SQLOrderItem(
            order_id=5,
            item_name='Salad',
            item_price=8.99,
            quantity=1
        )
        
        item_dict = item.to_dict()
        
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['item_name'], 'Salad')
        self.assertEqual(item_dict['quantity'], 1)


if __name__ == '__main__':
    unittest.main()