from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.delete("/items/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()

    db.delete(db_item)
    db.commit()

    return {"message": "Item terhapus"}