import math
import uuid
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from backend.db import delete_transaction, fetch_summary, fetch_transactions, insert_transaction

router = APIRouter()


class TransactionIn(BaseModel):
    amount: float
    category: str
    description: str = ""
    date: str

    @field_validator("amount")
    @classmethod
    def finite_amount(cls, v):
        if not math.isfinite(v):
            raise ValueError("amount must be a finite number")
        return v

    @field_validator("date")
    @classmethod
    def valid_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date must be YYYY-MM-DD")
        return v


@router.get("/transactions")
def list_transactions(month: Optional[str] = None, category: Optional[str] = None):
    return fetch_transactions(month, category)


@router.get("/summary")
def get_summary(month: Optional[str] = None):
    return fetch_summary(month)


@router.post("/transactions", status_code=201)
def add_transaction(body: TransactionIn):
    txn = {
        "id": str(uuid.uuid4()),
        "amount": body.amount,
        "category": body.category.lower().strip(),
        "description": body.description.strip(),
        "date": body.date,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    insert_transaction(txn)
    return txn


@router.delete("/transactions/{txn_id}", status_code=204)
def remove_transaction(txn_id: str):
    if not delete_transaction(txn_id):
        raise HTTPException(status_code=404, detail="Transaction not found")
