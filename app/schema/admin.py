from pydantic import BaseModel

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
