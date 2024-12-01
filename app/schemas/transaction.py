from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

# Перечисление для типа транзакции
class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

# Схема для добавления транзакции
class TransactionCreate(BaseModel):
    date: date
    type: TransactionType
    category: str
    place: str
    amount: float
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Схема для вывода транзакции
class TransactionOut(TransactionCreate):
    id: int

    class Config:
        from_attributes = True