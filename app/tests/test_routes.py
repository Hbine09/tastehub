import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestRoutes(unittest.TestCase):
    """Test cases for application routes"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CloudBite', response.data)
    
    def test_menu_page(self):
        """Test menu page loads"""
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Our Menu', response.data)
    
    def test_about_page(self):
        """Test about page loads"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About CloudBite', response.data)
    
    def test_api_docs_page(self):
        """Test API documentation page loads"""
        response = self.client.get('/api-docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'API Documentation', response.data)
    
    def test_login_page(self):
        """Test login page loads"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_register_page(self):
        """Test register page loads"""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
    
    def test_menu_api_endpoint(self):
        """Test menu API endpoint returns JSON"""
        response = self.client.get('/menu/api/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = response.get_json()
        self.assertIn('success', data)
        self.assertIn('items', data)
    
    def test_orders_api_requires_auth(self):
        """Test orders API requires authentication"""
        response = self.client.get('/orders/api/orders')
        self.assertEqual(response.status_code, 401)
        
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_create_order_requires_auth(self):
        """Test creating order requires authentication"""
        response = self.client.post('/orders/create',
                                   json={'items': []},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)


class TestAuthentication(unittest.TestCase):
    """Test cases for authentication"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_register_requires_all_fields(self):
        """Test registration requires all fields"""
        response = self.client.post('/auth/register', data={
            'email': 'test@example.com'
            # Missing name and password
        })
        self.assertEqual(response.status_code, 200)
        # Should stay on register page with error
        self.assertIn(b'Register', response.data)
    
    def test_login_requires_credentials(self):
        """Test login requires email and password"""
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com'
            # Missing password
        })
        self.assertEqual(response.status_code, 200)
        # Should stay on login page
        self.assertIn(b'Login', response.data)


if __name__ == '__main__':
    unittest.main()