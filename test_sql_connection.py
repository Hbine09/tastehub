import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Cloud SQL Connection...")
print("=" * 50)
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print("=" * 50)

try:
    from app.models.sql_models import get_db_session, SQLOrder
    
    print("Getting database session...")
    session = get_db_session()
    
    print("Querying orders...")
    orders = session.query(SQLOrder).all()
    
    print(f"✅ Success! Found {len(orders)} orders")
    session.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()