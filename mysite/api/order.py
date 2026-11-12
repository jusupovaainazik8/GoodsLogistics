from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from mysite.database.db import get_db
from mysite.database.models import Order, Product

router = APIRouter(prefix="/orders", tags=["Order"])


class OrderCreate(BaseModel):
    product_id: int
    user_id: int
    city_id: int
    quantity: int = 1


class OrderResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    city_id: int
    quantity: int
    total_price: float
    created_date: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    computed_total = product.price * order.quantity

    db_order = Order(
        product_id=order.product_id,
        user_id=order.user_id,
        city_id=order.city_id,
        quantity=order.quantity,
        total_price=computed_total,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    ord_obj = db.query(Order).filter(Order.id == order_id).first()
    if not ord_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return ord_obj


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderCreate, db: Session = Depends(get_db)):
    ord_obj = db.query(Order).filter(Order.id == order_id).first()
    if not ord_obj:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(Product).filter(Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    ord_obj.product_id = order_data.product_id
    ord_obj.user_id = order_data.user_id
    ord_obj.city_id = order_data.city_id
    ord_obj.quantity = order_data.quantity
    ord_obj.total_price = product.price * order_data.quantity

    db.commit()
    db.refresh(ord_obj)
    return ord_obj


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    ord_obj = db.query(Order).filter(Order.id == order_id).first()
    if not ord_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(ord_obj)
    db.commit()