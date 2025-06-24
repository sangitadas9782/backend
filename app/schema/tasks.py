from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int
    course_id: int

class TaskUpdate(BaseModel):
    is_completed: bool

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    user_id: int
    course_id: int

    class Config:
        orm_mode = True
