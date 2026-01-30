from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models.sql_models import get_db_session, SQLOrder, SQLOrderItem
from datetime import datetime

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/')
def order_list():
    """View user's orders from SQL database"""
    if 'user_id' not in session:
        flash('Please login to view orders', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    try:
        # Get orders from Cloud SQL
        db_session = get_db_session()
        sql_orders = db_session.query(SQLOrder).filter_by(user_id=user_id).order_by(SQLOrder.created_at.desc()).all()
        
        # Convert to dict for template
        user_orders = [order.to_dict() for order in sql_orders]
        
        db_session.close()
        
    except Exception as e:
        print(f"Error fetching orders from SQL: {e}")
        user_orders = []
        flash('Error loading orders', 'error')
    
    return render_template('orders/order_list.html', orders=user_orders)

@bp.route('/create', methods=['GET', 'POST'])
def create_order():
    """Create a new order - displays order form or processes submission"""
    if 'user_id' not in session:
        flash('Please login to place an order', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        # Display order creation form
        return render_template('orders/create_order.html')
    
    # POST request - process order
    try:
        data = request.get_json() if request.is_json else request.form
        items = data.get('items', [])
        
        if not items:
            return jsonify({'success': False, 'error': 'No items in order'}), 400
        
        # Calculate total
        total = 0
        for item in items:
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 1))
            total += price * quantity
        
        # Create order in Cloud SQL
        db_session = get_db_session()
        
        new_order = SQLOrder(
            user_id=session['user_id'],
            user_name=session['user_name'],
            user_email=session['user_email'],
            total=total,
            status='pending'
        )
        
        db_session.add(new_order)
        db_session.flush()  # Get the order ID
        
        # Add order items
        for item in items:
            order_item = SQLOrderItem(
                order_id=new_order.id,
                item_name=item.get('name'),
                item_price=float(item.get('price')),
                quantity=int(item.get('quantity', 1))
            )
            db_session.add(order_item)
        
        db_session.commit()
        order_id = new_order.id
        db_session.close()
        
        # Also save to Firestore for demonstration of multi-database usage
        order_data = {
            'sql_order_id': order_id,
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            'created_at': datetime.utcnow(),
            'status': 'pending'
        }
        db.collection('order_logs').add(order_data)
        
        if request.is_json:
            return jsonify({
                'success': True,
                'order_id': order_id,
                'message': 'Order created successfully'
            })
        else:
            flash('Order placed successfully!', 'success')
            return redirect(url_for('orders.order_list'))
        
    except Exception as e:
        print(f"Error creating order: {e}")
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash('Error placing order. Please try again.', 'error')
            return redirect(url_for('menu.menu_list'))

@bp.route('/<int:order_id>')
def order_detail(order_id):
    """View detailed information about a specific order"""
    if 'user_id' not in session:
        flash('Please login to view orders', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        db_session = get_db_session()
        order = db_session.query(SQLOrder).filter_by(id=order_id, user_id=session['user_id']).first()
        
        if not order:
            flash('Order not found', 'error')
            db_session.close()
            return redirect(url_for('orders.order_list'))
        
        order_dict = order.to_dict()
        db_session.close()
        
        return render_template('orders/order_detail.html', order=order_dict)
        
    except Exception as e:
        print(f"Error fetching order detail: {e}")
        flash('Error loading order details', 'error')
        return redirect(url_for('orders.order_list'))

@bp.route('/api/orders')
def api_orders():
    """REST API endpoint for user's orders"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        db_session = get_db_session()
        orders = db_session.query(SQLOrder).filter_by(user_id=session['user_id']).all()
        orders_list = [order.to_dict() for order in orders]
        db_session.close()
        
        return jsonify({
            'success': True,
            'orders': orders_list,
            'count': len(orders_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500