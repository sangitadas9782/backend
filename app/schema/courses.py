from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    name: str
    description: str

class CourseCreate(CourseBase):
    enrolment_fee: int = 0
    tasks: int = 0
    total_task_cost: int = 0
    is_active: bool = True

class CourseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    enrolment_fee: int | None = None
    tasks: int | None = None
    total_task_cost: int | None = None
    is_active: bool | None = None

class Course(CourseBase):
    id: int
    enrolment_fee: int
    tasks: int
    total_task_cost: int
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True