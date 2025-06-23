from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(36), unique=True)  # Store UUID as string
    user_email = Column(String(255), nullable=False)
    course_id = Column(Integer)
    course_name = Column(String(255))
    
    # Financial details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    # Transaction info
    transaction_type = Column(String(20), nullable=False)
    payment_status = Column(String(20), default="pending")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Renamed from 'metadata' to avoid conflict
    transaction_data = Column(String)  # Store JSON as text