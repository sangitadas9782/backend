from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from datetime import datetime

class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String,index=True, nullable=False)
    enrolment_fee = Column(Integer,index=True)
    tasks = Column(Integer,index=True)
    total_task_cost = Column(Integer,index=True)
    created_at = Column(DateTime, index=True, default=datetime.utcnow, nullable=False)    
    is_active = Column(Boolean, index=True, nullable=False, default=True)
