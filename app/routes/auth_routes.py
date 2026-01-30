from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
import bcrypt
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # Validate input
        if not email or not password or not name:
            flash('All fields are required', 'error')
            return render_template('auth/register.html')
        
        try:
            # Check if user already exists
            users_ref = db.collection('users')
            existing_user = users_ref.where('email', '==', email).limit(1).get()
            
            if len(list(existing_user)) > 0:
                flash('Email already registered', 'error')
                return render_template('auth/register.html')
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user document
            user_data = {
                'email': email,
                'password': hashed_password.decode('utf-8'),
                'name': name,
                'role': 'customer',
                'created_at': datetime.utcnow()
            }
            
            # Add to Firestore
            doc_ref = users_ref.add(user_data)
            user_id = doc_ref[1].id
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            print(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html')
        
        try:
            # Find user by email
            users_ref = db.collection('users')
            user_docs = users_ref.where('email', '==', email).limit(1).get()
            
            user_list = list(user_docs)
            if len(user_list) == 0:
                flash('Invalid email or password', 'error')
                return render_template('auth/login.html')
            
            user_doc = user_list[0]
            user_data = user_doc.to_dict()
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                # Set session
                session['user_id'] = user_doc.id
                session['user_email'] = user_data['email']
                session['user_name'] = user_data['name']
                session['user_role'] = user_data['role']
                
                flash(f'Welcome back, {user_data["name"]}!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Invalid email or password', 'error')
                return render_template('auth/login.html')
                
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login failed. Please try again.', 'error')
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.home'))