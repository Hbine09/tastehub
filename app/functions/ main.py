import functions_framework
from google.cloud import firestore
import json
from datetime import datetime

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
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        # Get request data
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return (json.dumps({'error': 'No data provided'}), 400, headers)
        
        order_id = request_json.get('order_id')
        user_email = request_json.get('user_email')
        user_name = request_json.get('user_name')
        total = request_json.get('total')
        items_count = request_json.get('items_count', 0)
        
        if not all([order_id, user_email, user_name]):
            return (json.dumps({'error': 'Missing required fields'}), 400, headers)
        
        # Log notification to Firestore
        notification_data = {
            'order_id': order_id,
            'user_email': user_email,
            'user_name': user_name,
            'total': total,
            'items_count': items_count,
            'status': 'sent',
            'timestamp': datetime.utcnow(),
            'type': 'order_confirmation',
            'message': f'Order #{order_id} confirmed for {user_name}. Total: ${total:.2f}'
        }
        
        # Save to Firestore notifications collection
        doc_ref = db.collection('notifications').add(notification_data)
        
        response_data = {
            'success': True,
            'message': f'Notification sent to {user_email}',
            'order_id': order_id,
            'notification_id': doc_ref[1].id
        }
        
        return (json.dumps(response_data), 200, headers)
        
    except Exception as e:
        error_response = {'error': str(e), 'success': False}
        return (json.dumps(error_response), 500, headers)


@functions_framework.http
def get_order_stats(request):
    """
    HTTP Cloud Function to get order statistics.
    Returns analytics about orders from Firestore.
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
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        # Get all order logs from Firestore
        orders_ref = db.collection('order_logs')
        orders = list(orders_ref.stream())
        
        total_orders = len(orders)
        
        # Get notifications count
        notifications_ref = db.collection('notifications')
        notifications = list(notifications_ref.stream())
        total_notifications = len(notifications)
        
        # Get menu items count
        menu_ref = db.collection('menu_items')
        menu_items = list(menu_ref.stream())
        total_menu_items = len(menu_items)
        
        analytics = {
            'success': True,
            'total_orders': total_orders,
            'total_notifications': total_notifications,
            'total_menu_items': total_menu_items,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return (json.dumps(analytics), 200, headers)
        
    except Exception as e:
        error_response = {'error': str(e), 'success': False}
        return (json.dumps(error_response), 500, headers)