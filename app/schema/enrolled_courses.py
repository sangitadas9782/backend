from pydantic import BaseModel
from datetime import datetime

class EnrollmentBase(BaseModel):
    course_id: int
    user_email: str
class EnrollmentCreate(EnrollmentBase):
    course_name: str
class EnrollmentUpdate(EnrollmentBase):
    pass  # Just needs course_id and user_email
class EnrollmentResponse(EnrollmentBase):
    id: int
    course_name: str
    enrolled_at: datetime
    is_complete: bool
    class Config:
        orm_mode = True