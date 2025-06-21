from fastapi import FastAPI, Depends
from app.schema.items import Item, ItemCreate
from app.schema.users import User, UserCreate
from app.controllers.items import ItemController
from app.controllers.users import UserController
from app.database import get_db, engine
from app.models.items import Item as ItemModel

# Create tables
ItemModel.metadata.create_all(bind=engine)

app = FastAPI()
controller = ItemController()
userController = UserController()

@app.get("/")
def hello():
    return "hello World"

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db=Depends(get_db)):
    return controller.create_item(item, db)

@app.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return controller.read_items(skip, limit, db)

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db=Depends(get_db)):
    return controller.read_item(item_id, db)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, db=Depends(get_db)):
    return controller.update_item(item_id, item, db)

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int, db=Depends(get_db)):
    return controller.delete_item(item_id, db)


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