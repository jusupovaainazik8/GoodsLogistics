from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from mysite.database.db import get_db
from mysite.database.models import Store

router = APIRouter(prefix="/stores", tags=["Store"])


class StoreCreate(BaseModel):
    store_name: str
    category_id: int
    store_image: Optional[str] = None


class StoreResponse(BaseModel):
    id: int
    store_name: str
    category_id: int
    store_image: Optional[str]

    class Config:
        from_attributes = True


@router.get("/", response_model=List[StoreResponse])
def list_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    db_store = Store(**store.model_dump())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.put("/{store_id}", response_model=StoreResponse)
def update_store(store_id: int, store_data: StoreCreate, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    for key, val in store_data.model_dump().items():
        setattr(store, key, val)
    db.commit()
    db.refresh(store)
    return store


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(store)
    db.commit()