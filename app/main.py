from fastapi import FastAPI, Depends
from app.schema.items import Item, ItemCreate
from app.controllers.items import ItemController
from app.database import get_db, engine
from app.models.items import Item as ItemModel

# Create tables
ItemModel.metadata.create_all(bind=engine)

app = FastAPI()
controller = ItemController()

@app.get("/")
def hello():
    return "hello"

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