from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.models.enrolled_courses import   EnrolledCourses

class EnrolledCoursesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_email(self, user_email: str) -> List[EnrolledCourses]:
        """Get all EnrolledCourses enrolled by a specific user"""
        return self.db.query(EnrolledCourses).filter(
            EnrolledCourses.user_email == user_email
        ).all()

    def get_by_course_id(self, course_id: int) -> List[EnrolledCourses]:
        """Get all users enrolled in a specific course"""
        return self.db.query(EnrolledCourses).filter(
            EnrolledCourses.course_id == course_id
        ).all()

    def get_enrollment(self, user_email: str, course_id: int) -> Optional[EnrolledCourses]:
        """Get specific enrollment record"""
        return self.db.query(EnrolledCourses).filter(
            EnrolledCourses.user_email == user_email,
            EnrolledCourses.course_id == course_id
        ).first()

    def enroll_user(self, user_email: str, course_id: int, course_name: str) -> EnrolledCourses:
        """Enroll a user in a course"""
        enrollment = EnrolledCourses(
            course_name=course_name,
            course_id=course_id,
            user_email=user_email,
            enrolled_at=datetime.utcnow(),
            is_complete=False
        )
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def complete_course(self, user_email: str, course_id: int) -> Optional[EnrolledCourses]:
        """Mark a course as complete for a user"""
        enrollment = self.get_enrollment(user_email, course_id)
        if not enrollment:
            return None
        
        enrollment.is_complete = True
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def get_active_enrollments(self, user_email: str) -> List[EnrolledCourses]:
        """Get all active (incomplete) enrollments for a user"""
        return self.db.query(EnrolledCourses).filter(
            EnrolledCourses.user_email == user_email,
            EnrolledCourses.is_complete == False
        ).all()

    def get_completed_enrollments(self, user_email: str) -> List[EnrolledCourses]:
        """Get all completed enrollments for a user"""
        return self.db.query(EnrolledCourses).filter(
            EnrolledCourses.user_email == user_email,
            EnrolledCourses.is_complete == True
        ).all()