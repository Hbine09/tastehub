from flask import Blueprint, render_template, jsonify
from app import db

bp = Blueprint('menu', __name__, url_prefix='/menu')

@bp.route('/')
def menu_list():
    """Display all menu items"""
    menu_ref = db.collection('menu_items')
    menu_items = []
    
    try:
        docs = menu_ref.stream()
        for doc in docs:
            item = doc.to_dict()
            item['id'] = doc.id
            menu_items.append(item)
    except Exception as e:
        print(f"Error fetching menu: {e}")
    
    # Group by category
    categories = {}
    for item in menu_items:
        category = item.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    return render_template('menu/menu_list.html', categories=categories)

@bp.route('/api/items')
def api_menu_items():
    """REST API endpoint for menu items"""
    menu_ref = db.collection('menu_items')
    menu_items = []
    
    try:
        docs = menu_ref.stream()
        for doc in docs:
            item = doc.to_dict()
            item['id'] = doc.id
            menu_items.append(item)
        
        return jsonify({
            'success': True,
            'items': menu_items,
            'count': len(menu_items)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500