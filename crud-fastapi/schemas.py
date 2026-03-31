from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemResponse(ItemBase):
    id: int

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True