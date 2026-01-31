from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app import db
from app.utils.storage import upload_image, list_images
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin email list - only these emails can access admin features
ADMIN_EMAILS = [
    '',
    # Add your email here for testing
    'your-email@example.com'  # Replace with your actual email
]

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('auth.login'))
        
        # Check if user is admin
        user_email = session.get('user_email')
        if user_email not in ADMIN_EMAILS:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.home'))
        
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/upload-menu-image', methods=['GET', 'POST'])
@admin_required
def upload_menu_image():
    """Upload image for menu item - ADMIN ONLY"""
    
    if request.method == 'POST':
        menu_item_id = request.form.get('menu_item_id')
        image_file = request.files.get('image')
        
        if not menu_item_id or not image_file:
            flash('Please select both menu item and image', 'error')
            return redirect(url_for('admin.upload_menu_image'))
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(image_file.filename)
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            flash('Invalid file type. Please upload an image file.', 'error')
            return redirect(url_for('admin.upload_menu_image'))
        
        # Validate file size (max 5MB)
        image_file.seek(0, 2)  # Seek to end
        file_size = image_file.tell()  # Get size
        image_file.seek(0)  # Reset to beginning
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            flash('File too large. Maximum size is 5MB.', 'error')
            return redirect(url_for('admin.upload_menu_image'))
        
        # Upload to Cloud Storage
        try:
            image_url = upload_image(image_file, folder='menu')
            
            if image_url:
                # Update Firestore menu item with image URL
                menu_ref = db.collection('menu_items').document(menu_item_id)
                menu_ref.update({'image_url': image_url})
                
                flash('✅ Image uploaded successfully!', 'success')
                return redirect(url_for('admin.upload_menu_image'))
            else:
                flash('Failed to upload image', 'error')
                
        except Exception as e:
            print(f"Upload error: {e}")
            flash('Error uploading image', 'error')
    
    # GET request - show form
    try:
        # Get all menu items
        menu_ref = db.collection('menu_items')
        menu_items = []
        docs = menu_ref.stream()
        
        for doc in docs:
            item = doc.to_dict()
            item['id'] = doc.id
            menu_items.append(item)
        
        # Sort by name
        menu_items.sort(key=lambda x: x.get('name', ''))
        
        # Get recently uploaded images
        uploaded_images = list_images(folder='menu')[:12]  # Last 12 images
        
        return render_template('admin/upload_menu_image.html', 
                             menu_items=menu_items,
                             uploaded_images=uploaded_images)
        
    except Exception as e:
        print(f"Error loading admin page: {e}")
        flash('Error loading page', 'error')
        return redirect(url_for('main.home'))


@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard - ADMIN ONLY"""
    
    try:
        # Get stats
        menu_count = len(list(db.collection('menu_items').stream()))
        users_count = len(list(db.collection('users').stream()))
        orders_count = len(list(db.collection('order_logs').stream()))
        notifications_count = len(list(db.collection('notifications').stream()))
        
        stats = {
            'menu_items': menu_count,
            'users': users_count,
            'orders': orders_count,
            'notifications': notifications_count
        }
        
        return render_template('admin/dashboard.html', stats=stats)
        
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('main.home'))