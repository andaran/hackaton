from fastapi import FastAPI
from routes import auth, transactions
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, transactions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
