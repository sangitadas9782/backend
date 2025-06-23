from sqlalchemy.orm import Session
from app.models.users import User
from app.schema.users import UserCreate  
from app.schema.users import UserBase  

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_user(self, email:str):
        return self.db.query(User).filter(User.email == email).first()
    def get_users(self, skip: int = 0, limit: int = 100):
        """Get a list of users."""
        return self.db.query(User).offset(skip).limit(limit).all()
    def create_user(self, user_data: UserCreate):
        """Create a new user from a UserCreate schema."""
        db_user = User(**user_data.dict()) 
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    def update_user(self, email: str, user_data: UserBase):
        db_user = self.db.query(User).filter(User.email == email).first()
        if db_user:
            for key, value in user_data.dict().items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    def delete_user(self, email: str):
        """Delete an existing user."""
        db_user = self.db.query(User).filter(User.email == email).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
