from pydantic import BaseModel
from typing import Optional

#! Product
class ProductCreate(BaseModel):
    name:str
    price:int

class ProductUpdate(BaseModel):
    name: Optional[str]=None
    price: Optional[int]=None

class ProductOut(BaseModel):
    id:int
    name:str
    price:int
    class Config:
        orm_mode =True   


class ProductFilter(BaseModel):
    search:Optional[str] =None
    min_price:Optional[int] =None
    max_price :Optional[int]=None
    sort_by:Optional[str]="id"
    sort_order:Optional[str]="asc"
    page:Optional[int]=1
    limit:Optional[int]=10

#! Order
class OrderCreate(BaseModel):

    user_id:int
    total_amount:int

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: int
    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    total_amount: Optional[int] = None

class OrderFilter(BaseModel):
    search:Optional[str] =None
    min_amt:Optional[int] =None
    max_amt :Optional[int]=None
    sort_by:Optional[str]="id"
    sort_order:Optional[str]="asc"
    page:Optional[int]=1
    limit:Optional[int]=10



#!OrderItem
class OrderItemCreate(BaseModel):

    order_id : int
    product_id:int
    quantity:int
    price:int

class OrderItemUpdate(BaseModel):
    quantity:Optional[int]=None
    price:Optional[int]=None

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: int
    class Config:
        orm_mode = True

class OrderItemFilter(BaseModel):
    search:Optional[str] =None
    min_price:Optional[int] =None
    max_price :Optional[int]=None
    sort_by:Optional[str]="id"
    sort_order:Optional[str]="asc"
    page:Optional[int]=1
    limit:Optional[int]=10

#!CartItem
class CartItemCreate(BaseModel):

    user_id : int
    product_id:int
    quantity:int

class CartItemUpdate(BaseModel):
    quantity:Optional[int]=None

class CartItemOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    class Config:
        orm_mode = True

class CartItemFilter(BaseModel):
    search:Optional[str] =None
    sort_by :Optional[str]="id"
    sort_order:Optional[str]="asc"
    page:Optional[int]=1
    limit:Optional[int]=10
    