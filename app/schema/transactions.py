from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class TransactionBase(BaseModel):
    user_email: str = Field(..., example="student@example.com")
    course_id: int = Field(..., example=101)
    amount: float = Field(..., example=99.99)
    transaction_type: str = Field(..., example="purchase")

class TransactionCreate(TransactionBase):
    course_name: Optional[str] = Field(None, example="Advanced Python")
    currency: Optional[str] = Field("USD", example="USD")
    metadata: Optional[dict] = Field({}, example={"payment_method": "credit_card"})

class TransactionUpdate(BaseModel):
    new_status: str = Field(..., example="completed")
    metadata: Optional[dict] = Field(None, example={"refund_reason": "duplicate"})

class TransactionResponse(TransactionBase):
    transaction_id: str = Field(..., example=str(uuid.uuid4()))
    course_name: Optional[str]
    currency: str
    payment_status: str = Field(..., example="pending")
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True