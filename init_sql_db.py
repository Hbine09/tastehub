import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models.sql_models import init_db

if __name__ == '__main__':
    print("=" * 50)
    print("Initializing Cloud SQL Database")
    print("=" * 50)
    print()
    
    try:
        init_db()
        print()
        print("=" * 50)
        print("Database initialized successfully!")
        print("=" * 50)
    except Exception as e:
        print(f"\n Error initializing database: {e}")
        import traceback
        traceback.print_exc()