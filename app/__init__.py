import os
from flask import Flask
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
from app.routes import main_routes, auth_routes, order_routes, menu_routes, admin_routes

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Import routes (we'll create these later)
from app.routes import main_routes, auth_routes, order_routes, menu_routes

# Register blueprints
app.register_blueprint(main_routes.bp)
app.register_blueprint(auth_routes.bp)
app.register_blueprint(order_routes.bp)
app.register_blueprint(menu_routes.bp)
app.register_blueprint(admin_routes.bp)