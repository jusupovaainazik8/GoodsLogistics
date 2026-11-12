from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

from mysite.database.db import get_db
from mysite.database.models import Review

router = APIRouter(prefix="/reviews", tags=["Review"])


class ReviewCreate(BaseModel):
    store_id: int
    user_id: int
    text: str
    stars: int = Field(..., ge=1, le=5)


class ReviewResponse(BaseModel):
    id: int
    store_id: int
    user_id: int
    text: str
    stars: int
    created_date: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ReviewResponse])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    rev = db.query(Review).filter(Review.id == review_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Review not found")
    return rev


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_data: ReviewCreate, db: Session = Depends(get_db)):
    rev = db.query(Review).filter(Review.id == review_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, val in review_data.model_dump().items():
        setattr(rev, key, val)
    db.commit()
    db.refresh(rev)
    return rev


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    rev = db.query(Review).filter(Review.id == review_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(rev)
    db.commit()