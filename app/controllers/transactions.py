from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema.transactions import TransactionCreate, TransactionUpdate, TransactionResponse
from app.repository.transactions import TransactionRepository
from app.database import get_db

transationRouter = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)
@transationRouter.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    repo = TransactionRepository(db)
    try:
        return repo.create(transaction)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@transationRouter.get("/user/{user_email}", response_model=list[TransactionResponse])
def get_user_transactions(
    user_email: str,
    db: Session = Depends(get_db)
):
    repo = TransactionRepository(db)
    return repo.get_by_user(user_email)

@transationRouter.patch("/{transaction_id}/status", response_model=TransactionResponse)
def update_status(
    transaction_id: str,
    status_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    repo = TransactionRepository(db)
    transaction = repo.update_status(transaction_id, status_update.new_status)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction