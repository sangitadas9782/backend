from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schema.admin import AdminLogin
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()

def authenticate_admin(db: Session, login_data: AdminLogin):
    admin = get_admin_by_email(db, login_data.email)
    if not admin or not verify_password(login_data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return admin
