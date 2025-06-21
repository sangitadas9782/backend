from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.schema.users import User, UserCreate
from app.repository.users import UserRepository
from app.database import get_db

class UserController:
    def __init__(self):
        self.repository = UserRepository

    def read_users(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        """Retrieve a list of users, paging through results."""
        return self.repository(db).get_users(skip, limit)

    def read_user(self, email:str, db: Session = Depends(get_db)):
        """Get a specific user by ID, or raise 404 if not found."""
        db_user = self.repository(db).get_user(email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    def create_user(self, user: UserCreate, db: Session = Depends(get_db)):
        """Create a new user record."""
        return self.repository(db).create_user(user)

    def update_user(self, email: str, user: UserCreate, db: Session = Depends(get_db)):
        """Update an existing user record, or raise 404 if not found."""
        db_user = self.repository(db).get_user(email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repository(db).update_user(email, user)

    def delete_user(self, email: str, db: Session = Depends(get_db)):
        """Delete a user record, or raise 404 if not found."""
        db_user = self.repository(db).get_user(email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repository(db).delete_user(email)
