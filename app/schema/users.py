from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    password: str
    address: str
    email: str
    is_active: bool   
class UserCreate(UserBase):
    pass
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True