from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True