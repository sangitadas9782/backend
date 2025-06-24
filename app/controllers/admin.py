from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.admin import AdminLogin, AdminOut
from app.repository.admin import authenticate_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login", response_model=AdminOut)
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    return authenticate_admin(db, login_data)
