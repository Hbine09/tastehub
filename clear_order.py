import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models.sql_models import get_db_session, SQLOrder, SQLOrderItem

if __name__ == '__main__':
    print("Clearing all orders...")
    
    try:
        session = get_db_session()
        
        # Delete all order items
        deleted_items = session.query(SQLOrderItem).delete()
        print(f"Deleted {deleted_items} order items")
        
        # Delete all orders
        deleted_orders = session.query(SQLOrder).delete()
        print(f"Deleted {deleted_orders} orders")
        
        session.commit()
        session.close()
        
        print("✅ All orders cleared successfully!")
        print("You can now place new orders that will work correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()