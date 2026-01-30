from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class SQLOrder(Base):
    """SQL Model for Orders - stored in Cloud SQL PostgreSQL"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String(50), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to order items
    order_items = relationship('SQLOrderItem', back_populates='order', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert order to dictionary with items"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'items': [item.to_dict() for item in self.order_items]  # Changed from self.items
        }

class SQLOrderItem(Base):
    """SQL Model for Order Items"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_name = Column(String(100), nullable=False)
    item_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Relationship back to order
    order = relationship('SQLOrder', back_populates='order_items')  # Changed from 'items'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_name': self.item_name,
            'item_price': self.item_price,
            'quantity': self.quantity
        }

# Database connection helper
def get_db_engine():
    """Create database engine for Cloud SQL"""
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    
    # Connection string for PostgreSQL
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    engine = create_engine(connection_string)
    return engine

def get_db_session():
    """Get database session"""
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    """Initialize database tables"""
    engine = get_db_engine()
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully!")