from sqlalchemy.orm import Session
from datetime import datetime
from app.models.courses import Courses 
class CourseRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_by_id(self, course_id: int) -> Courses | None:
        """Get a course by its ID"""
        return self.db.query(Courses).filter(Courses.id == course_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Courses]:
        """Get all courses with pagination"""
        return self.db.query(Courses).offset(skip).limit(limit).all()

    def create(self, course_data: dict) -> Courses:
        """Create a new course"""
        course = Courses(
            name=course_data['name'],
            description=course_data['description'],
            enrolment_fee=course_data.get('enrolment_fee', 0),
            tasks=course_data.get('tasks', 0),
            total_task_cost=course_data.get('total_task_cost', 0),
            created_at=datetime.utcnow(),
            is_active=course_data.get('is_active', True)
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def update(self, course_id: int, update_data: dict) -> Courses | None:
        """Update a course"""
        course = self.get_by_id(course_id)
        if not course:
            return None
        
        for key, value in update_data.items():
            setattr(course, key, value)
        
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete(self, course_id: int) -> bool:
        """Delete a course (soft delete by setting is_active=False)"""
        course = self.get_by_id(course_id)
        if not course:
            return False    
        course.is_active = False
        self.db.commit()
        return True
    def search_by_name(self, name: str) -> list[Courses]:
        """Search courses by name (case-insensitive partial match)"""
        return self.db.query(Courses).filter(
            Courses.name.ilike(f"%{name}%"),
            Courses.is_active == True
        ).all()