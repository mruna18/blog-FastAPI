from fastapi import FastAPI
from app.blog.routes import router
from app.category.routes import category_router
from app.users.router import user_router
from app.database import Base,engine
from app.order.routes import order_router


app = FastAPI()
app.include_router(router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(order_router)



