from flask import Blueprint, render_template, session
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    """Home page - shows restaurant info and featured items"""
    # Get featured menu items from Firestore
    menu_ref = db.collection('menu_items')
    featured_items = []
    
    try:
        # Get first 6 items as featured
        docs = menu_ref.limit(6).stream()
        for doc in docs:
            item = doc.to_dict()
            item['id'] = doc.id
            featured_items.append(item)
    except Exception as e:
        print(f"Error fetching featured items: {e}")
    
    return render_template('home.html', featured_items=featured_items)

@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@bp.route('/api-docs')
def api_docs():
    """API Documentation page"""
    return render_template('api_docs.html')