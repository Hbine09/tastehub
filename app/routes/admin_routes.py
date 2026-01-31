from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.utils.storage import upload_image, list_images
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Simple admin check (you can enhance this)
def is_admin():
    """Check if user is admin"""
    return session.get('user_role') == 'staff' or session.get('user_email') == 'admin@cloudbite.com'

@bp.route('/upload-menu-image', methods=['GET', 'POST'])
def upload_menu_image():
    """Upload image for menu item"""
    
    # Check authentication
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'error')
        return redirect(url_for('auth.login'))
    
    # For demo purposes, allow any logged-in user
    # In production, you'd check: if not is_admin(): return redirect(...)
    
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
        
        # Upload to Cloud Storage
        try:
            image_url = upload_image(image_file, folder='menu')
            
            if image_url:
                # Update Firestore menu item with image URL
                menu_ref = db.collection('menu_items').document(menu_item_id)
                menu_ref.update({'image_url': image_url})
                
                flash('Image uploaded successfully!', 'success')
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
def dashboard():
    """Simple admin dashboard"""
    if 'user_id' not in session:
        flash('Please login to access admin panel', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Get stats
        menu_count = len(list(db.collection('menu_items').stream()))
        users_count = len(list(db.collection('users').stream()))
        orders_count = len(list(db.collection('order_logs').stream()))
        
        stats = {
            'menu_items': menu_count,
            'users': users_count,
            'orders': orders_count
        }
        
        return render_template('admin/dashboard.html', stats=stats)
        
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('main.home'))