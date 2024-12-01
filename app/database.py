from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base as UserBase
from models.transaction import Base as TransactionBase
import os

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL не установлена!")

DATABASE_URL = "mysql+mysqlconnector://root:rootpassword@host.docker.internal:3306/finance_db"

# Настройка SQLAlchemy
engine = create_engine(DATABASE_URL)

# DATABASE_URL = "mysql+mysqlconnector://root:rootpassword@localhost/finance_db"

# engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц в базе данных
UserBase.metadata.create_all(bind=engine)
TransactionBase.metadata.create_all(bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()