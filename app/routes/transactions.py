from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, inspect
from models.user import User
from models.transaction import get_user_transaction_table
from database import get_db, engine
from schemas.transaction import TransactionCreate, TransactionOut
from sqlalchemy import desc

router = APIRouter()

@router.post("/{user_id}/", response_model=TransactionOut)
async def add_transaction(user_id: str, transaction: TransactionCreate, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Проверка существования пользователя
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Валидация типа транзакции
    if transaction.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Создание таблицы, если она не существует
    if not inspect(engine).has_table(Transaction.__tablename__):
        Transaction.__table__.create(bind=engine)

    # Добавляем транзакцию в таблицу
    db_transaction = Transaction(
        date=transaction.date,
        type=transaction.type,
        category=transaction.category,
        place=transaction.place,
        amount=transaction.amount,
        description=transaction.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/{user_id}/", response_model=list[TransactionOut])
async def get_transactions(user_id: str, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Если таблица не существует, то возвращаем ошибку
    if not inspect(engine).has_table(Transaction.__tablename__):
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    transactions = db.query(Transaction).order_by(desc(Transaction.date)).all()
    return transactions

@router.delete("/{user_id}/{transaction_id}/")
async def delete_transaction(user_id: str, transaction_id: int, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Если таблица не существует, то возвращаем ошибку
    if not inspect(engine).has_table(Transaction.__tablename__):
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@router.get("/{user_id}/{start_date}/{end_date}/", response_model=list[TransactionOut])
async def get_transactions_by_period(user_id: str, start_date: str, 
                                     end_date: str, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Если таблица не существует, то возвращаем ошибку
    if not inspect(engine).has_table(Transaction.__tablename__):
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    transactions = db.query(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).order_by(desc(Transaction.date)).all()

    return transactions