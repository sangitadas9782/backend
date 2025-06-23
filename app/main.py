from fastapi import FastAPI, Depends
from app.schema.users import User, UserCreate
from app.controllers.users import UserController
from app.controllers.courses import courseRouter
from app.controllers.enrolled_courses import enrollmentRouter
from app.controllers.transactions import transationRouter
from app.database import get_db, engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

userController = UserController()
app.include_router(courseRouter)
app.include_router(enrollmentRouter)
app.include_router(transationRouter)

@app.get("/")
def hello():
    return "hello World"


''' this is the user block below '''

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db=Depends(get_db)):
    return userController.create_user(user, db)

@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return userController.read_users(skip, limit, db)

@app.get("/users/{email}", response_model=User)
def read_users(email: str, db=Depends(get_db)):
    return userController.read_user(email, db)

@app.put("/users/{email}", response_model=User)
def update_user(email: str, user: UserCreate, db=Depends(get_db)):
    return userController.update_user(email, user, db)

@app.delete("/users/{email}", response_model=User)
def delete_user(email: str, db=Depends(get_db)):
    return userController.delete_user(email, db)