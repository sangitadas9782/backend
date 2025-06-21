from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.schema.courses import CourseCreate, CourseUpdate, Course
from app.repository.courses import CourseRepository
from app.database import get_db

courseRouter = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)


@courseRouter.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    try:
        return repo.create(course.dict())        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@courseRouter.get("/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    courses = repo.get_all(skip=skip, limit=limit)
    return [course for course in courses]

@courseRouter.get("/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    db_course = repo.get_by_id(course_id)
    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return db_course

@courseRouter.put("/{course_id}", response_model=Course)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):
    repo = CourseRepository(db)
    db_course = repo.update(course_id, course.dict(exclude_unset=True))
    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return db_course

@courseRouter.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    success = repo.delete(course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return None

@courseRouter.get("/search/", response_model=List[Course])
def search_courses(name: str, db: Session = Depends(get_db)):
    repo = CourseRepository(db)
    courses = repo.search_by_name(name)
    return [course for course in courses]