from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.schema.items import Item, ItemCreate
from app.repository.items import ItemRepository
from app.database import get_db

class ItemController:
    def __init__(self):
        self.repository = ItemRepository

    def read_items(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return self.repository(db).get_items(skip, limit)

    def read_item(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.repository(db).get_item(item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def create_item(self, item: ItemCreate, db: Session = Depends(get_db)):
        return self.repository(db).create_item(item)

    def update_item(self, item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
        db_item = self.repository(db).get_item(item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return self.repository(db).update_item(item_id, item)

    def delete_item(self, item_id: int, db: Session = Depends(get_db)):
        db_item = self.repository(db).get_item(item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return self.repository(db).delete_item(item_id)