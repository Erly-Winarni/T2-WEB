from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from utils import get_token_from_header
from fastapi import Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from auth import decode_token
from auth import hash_password, verify_password, create_token, decode_token

import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "CRUD API berjalan"}


@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    new_item = models.Item(
        name=item.name,
        description=item.description
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/items/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


@app.get("/items/{id}", response_model=schemas.ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    return db.query(models.Item).filter(models.Item.id == id).first()


@app.put("/items/{id}", response_model=schemas.ItemResponse)
def update_item(id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()

    db_item.name = item.name
    db_item.description = item.description

    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "username": db_user.username,
        "role": db_user.role
    })

    return {"access_token": token}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    return payload
@app.delete("/items/{id}")
def delete_item(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    db.delete(db_item)
    db.commit()

    return {"message": "Item terhapus"}