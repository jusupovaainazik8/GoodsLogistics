from fastapi import FastAPI
from mysite.database.db import Base, engine
from mysite.api import (
    users,
    category,
    city,
    store,
    product,
    review,
    order
)

from mysite.admin.views import setup_admin


Base.metadata.create_all(bind=engine)

app = FastAPI(title="GoodsLogistics API")


setup_admin(app)

app.include_router(users.router)
app.include_router(category.router)
app.include_router(city.router)
app.include_router(store.router)
app.include_router(product.router)
app.include_router(review.router)
app.include_router(order.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)