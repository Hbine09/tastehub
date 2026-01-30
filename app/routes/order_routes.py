from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from datetime import datetime

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/')
def order_list():
    """View user's orders"""
    if 'user_id' not in session:
        flash('Please login to view orders', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    orders_ref = db.collection('orders')
    user_orders = []
    
    try:
        docs = orders_ref.where('user_id', '==', user_id).order_by('created_at', direction='DESCENDING').stream()
        for doc in docs:
            order = doc.to_dict()
            order['id'] = doc.id
            user_orders.append(order)
    except Exception as e:
        print(f"Error fetching orders: {e}")
    
    return render_template('orders/order_list.html', orders=user_orders)

@bp.route('/create', methods=['POST'])
def create_order():
    """Create a new order"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({'success': False, 'error': 'No items in order'}), 400
        
        # Calculate total
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        
        # Create order document
        order_data = {
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            'user_email': session['user_email'],
            'items': items,
            'total': total,
            'status': 'pending',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Add to Firestore
        orders_ref = db.collection('orders')
        doc_ref = orders_ref.add(order_data)
        order_id = doc_ref[1].id
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Order created successfully'
        })
        
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500