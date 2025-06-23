from sqlalchemy.orm import Session
from app.models.transactions import Transaction
from app.schema.transactions import TransactionCreate
import json
import uuid

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self, transaction: TransactionCreate) -> Transaction:
        db_transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            user_email=transaction.user_email,
            course_id=transaction.course_id,
            course_name=transaction.course_name,
            amount=transaction.amount,
            currency=transaction.currency,
            transaction_type=transaction.transaction_type,            
            transaction_data=json.dumps(transaction.metadata or {}))
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    def get_by_user(self, user_email: str) -> list[Transaction]:
        return self.db.query(Transaction)\
                   .filter(Transaction.user_email == user_email)\
                   .order_by(Transaction.created_at.desc())\
                   .all()

    def update_status(self, transaction_id: str, new_status: str) -> Transaction:
        transaction = self.db.query(Transaction)\
                         .filter(Transaction.transaction_id == transaction_id)\
                         .first()
        if transaction:
            transaction.payment_status = new_status
            self.db.commit()
            self.db.refresh(transaction)
        return transaction