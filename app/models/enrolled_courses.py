from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from datetime import datetime

class EnrolledCourses(Base):
    __tablename__ = "enrolled_courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True, nullable=False)
    course_id = Column(Integer, index=True)
    user_email =  Column(String, index=True, nullable=False)  
    enrolled_at = Column(DateTime, index=True, default=datetime.utcnow, nullable=False)    
    is_complete = Column(Boolean, index=True, nullable=False, default=True)
