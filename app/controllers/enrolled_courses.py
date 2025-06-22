from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.schema.enrolled_courses import (
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate
)
from app.repository.enrolled_courses import EnrolledCoursesRepository
from app.database import get_db

enrollmentRouter = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"],
    responses={404: {"description": "Not found"}},
)


@enrollmentRouter.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_user(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    try:
        # Check if already enrolled
        existing = repo.get_enrollment(enrollment.user_email, enrollment.course_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already enrolled in this course"
            )
            
        db_enrollment = repo.enroll_user(
            user_email=enrollment.user_email,
            course_id=enrollment.course_id,
            course_name=enrollment.course_name
        )
        return db_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@enrollmentRouter.get("/user/{user_email}", response_model=List[EnrollmentResponse])
def get_user_enrollments(
    user_email: str,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    enrollments = repo.get_by_user_email(user_email)
    return [e for e in enrollments]

@enrollmentRouter.get("/course/{course_id}", response_model=List[EnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    enrollments = repo.get_by_course_id(course_id)
    return [e for e in enrollments]

@enrollmentRouter.patch("/complete", response_model=EnrollmentResponse)
def mark_course_complete(
    enrollment: EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    db_enrollment = repo.complete_course(enrollment.user_email, enrollment.course_id)
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return db_enrollment

@enrollmentRouter.get("/user/{user_email}/active", response_model=List[EnrollmentResponse])
def get_active_enrollments(
    user_email: str,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    enrollments = repo.get_active_enrollments(user_email)
    return [e for e in enrollments]

@enrollmentRouter.get("/user/{user_email}/completed", response_model=List[EnrollmentResponse])
def get_completed_enrollments(
    user_email: str,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    enrollments = repo.get_completed_enrollments(user_email)
    return [e for e in enrollments]

@enrollmentRouter.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def unenroll_user(
    enrollment: EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    repo = EnrolledCoursesRepository(db)
    # First get the enrollment to delete
    db_enrollment = repo.get_enrollment(enrollment.user_email, enrollment.course_id)
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Actually delete the record (or you could soft delete)
    db.delete(db_enrollment)
    db.commit()
    return None