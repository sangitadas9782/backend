from sqlalchemy.orm import Session
from app.models.items import Item

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_items(self, skip: int = 0, limit: int = 100):
        return self.db.query(Item).offset(skip).limit(limit).all()

    def create_item(self, item):
        db_item = Item(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update_item(self, item_id: int, item):
        db_item = self.db.query(Item).filter(Item.id == item_id).first()
        if db_item:
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def delete_item(self, item_id: int):
        db_item = self.db.query(Item).filter(Item.id == item_id).first()
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
        return db_item