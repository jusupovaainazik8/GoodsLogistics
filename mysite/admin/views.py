from sqladmin import ModelView
from mysite.database.models import (
    User,
    Category,
    Store,
    Product,
    Review,
    City,
    Order
)
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.status, User.created_date]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.store_name, Store.category, Store.store_image]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name, Product.store, Product.price, Product.is_original, Product.create_date]

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.store, Review.user, Review.stars, Review.created_date]

class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.city_name]

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.product, Order.user, Order.city, Order.quantity, Order.total_price, Order.created_date]


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(OrderAdmin)