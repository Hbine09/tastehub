import functions_framework
from google.cloud import firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Initialize Firestore
db = firestore.Client()

@functions_framework.http
def order_notification(request):
    """
    HTTP Cloud Function to send order notifications.
    Triggered when a new order is created.
    """
    
    # Enable CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    try:
        # Get request data
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return ({'error': 'No data provided'}, 400, headers)
        
        order_id = request_json.get('order_id')
        user_email = request_json.get('user_email')
        user_name = request_json.get('user_name')
        total = request_json.get('total')
        
        if not all([order_id, user_email, user_name, total]):
            return ({'error': 'Missing required fields'}, 400, headers)
        
        # Log notification to Firestore
        notification_data = {
            'order_id': order_id,
            'user_email': user_email,
            'user_name': user_name,
            'total': total,
            'status': 'sent',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'type': 'order_confirmation'
        }
        
        db.collection('notifications').add(notification_data)
        
        # In production, you would send actual email here
        # For this demo, we just log it
        
        return ({
            'success': True,
            'message': f'Notification sent to {user_email}',
            'order_id': order_id
        }, 200, headers)
        
    except Exception as e:
        return ({'error': str(e)}, 500, headers)


@functions_framework.http
def get_order_analytics(request):
    """
    HTTP Cloud Function to get order analytics.
    Returns statistics about orders.
    """
    
    # Enable CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    try:
        # Get all order logs from Firestore
        orders_ref = db.collection('order_logs')
        orders = orders_ref.stream()
        
        total_orders = 0
        total_revenue = 0
        
        for order in orders:
            total_orders += 1
            # Note: We'd need to query the SQL database for actual totals
            # This is a simplified version
        
        analytics = {
            'total_orders': total_orders,
            'status': 'active',
            'database': 'firestore'
        }
        
        return (analytics, 200, headers)
        
    except Exception as e:
        return ({'error': str(e)}, 500, headers)