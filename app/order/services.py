from sqlalchemy.orm import Session
from . import models,schemas
from sqlalchemy import or_,desc,asc
from fastapi import HTTPException,status
from app.users import models as m

#! Product
def create_product(db:Session,product:schemas.ProductCreate):
    products = models.Product(**product.dict())
    db.add(products)
    db.commit()
    db.refresh(products)
    return products

def get_product(db:Session,productid:int):
    return db.query(models.Product).filter(models.Product.id == productid).first()

def get_products(db:Session,skip:int=0, limit:int=10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def update_product(db:Session,product_id:int,product:schemas.ProductCreate):
    
    if not db.query(models.Product).filter(models.Product.id == product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="product id not found")
    
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    

    for var,value in vars(product).items():
        setattr(db_product,var,value)
        if not value is not None:
            setattr(db_product,var,value)

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db:Session,productid:int):
    product = db.query(models.Product).filter(models.Product.id == productid).first()

    if product:
        db.delete(product)
        db.commit()

    return product

def search_orders(db:Session,product:str):
    return db.query(models.Product).filter(models.Product.ilike(f"%{product}%")).all()

def get_paginated_product(db:Session,price:int=1,size:int=10):
    return db.query(models.Product).offset((price-1)*size).limit(size).all()

def get_all_products_advanced(db:Session,filters:schemas.ProductFilter):
    query=db.query(models.Product)
    if filters.search:
        search_terms=f"%{filters.search}%"
        query=query.filter(or_(models.Product.name.ilike(search_terms),models.Product.price.ilike(search_terms)))

    if filters.min_price is not None:
        query=query.filter(models.Product.price >= filters.min_price)

    if filters.max_price is not None:
        query=query.filter(models.Product.price <= filters.max_price)

    sort_column=getattr(models.Product,filters.sort_by,None)
    if sort_column is not None:
        sort_func =desc if filters.sort_order =="desc" else asc
        query = query.order_by (sort_func(sort_column))

    total =query.count()
    offset = (filters.page -1 )* filters.limit
    products = query.offset(offset).limit(filters.limit).all()

    return {
        "status":"success",
        "total":total,
        "page": filters.page,
        "limit":filters.limit,
        "data":products
    }

#! Order

def create_order(db:Session,order:schemas.ProductCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db:Session,orderid:int):
    return db.query(models.Order).filter(models.Order.id == orderid).first()

def get_orders(db:Session,skip:int=0,limit:int=10):
    return db.query(models.Order).offset(skip).limit(limit).all()

def update_order(db: Session,order_id:int,order:schemas.OrderUpdate):
    db_order=db.query(models.Order).filter(models.Order.id== order_id).first()
    if not db_order:
        return None
    
    for var,value in vars(order).items():
        setattr(db_order,var,value)
        if not value is not None:
            setattr(db_order,var,value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db:Session,id:int):
    db_order=db.query(models.Order).filter(models.Order.id==id).first()
    if  db_order:
        db.delete(db_order)
        db.commit()
    return db_order

def search_order(db:Session,amt:int):
    return db.query(models.Order).filter(models.Order.total_amount.ilike(f"%{amt}")).all()

def get_paginated_orders(db:Session,price:int=1,size:int=10):
    return db.query(models.Order).offser((price-1)* size).limit(size).all()
  

#! orderItem

def create_orderItem (db:Session,item:schemas.OrderItemCreate):
    db_orderItem = models.OrderItem(**item.dict())
    db.add(db_orderItem)
    db.commit()
    db.refresh(db_orderItem)
    return db_orderItem

def get_orderItem(db:Session,itemid:int):
    return db.query(models.OrderItem).filter(models.OrderItem.id == itemid).first()

def get_orderItems(db:Session,skip:int=0,limit:int=10):
    return db.query(models.OrderItem).offset(skip).limit(limit).all()

def update_orderItems(db:Session,itemid:int,item:schemas.OrderItemUpdate):
    db_item =db.query(models.OrderItem).filter(models.OrderItem.id == itemid).first()
    if not db_item:
        return None
    
    for var,value in vars(item).items():
        setattr(db_item,var,value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db:Session,itemid:int):
    db_item = db.query(models.OrderItem).filter(models.OrderItem.id == itemid).first()

    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def search_item(db:Session,qty:int):
    return db.query(models.OrderItem).filter(models.OrderItem.quantity.ilike(f"%{qty}")).all()

def get_paginated_items(db:Session,price:int=1,size:int=10):
    return db.query(models.OrderItem).offser((price-1)* size).limit(size).all()

def get_all_items_advanced(db:Session,filters:schemas.OrderItemFilter):
    query=db.query(models.OrderItem)
    if filters.search:
        search_term=f"%{filters.search}%"
        query=query.filter(models.OrderItem.quantity.ilike(search_term))
      

    if filters.min_price is not None:
        query=query.filter(models.OrderItem.price >= filters.min_price)

    if filters.max_price is not None:
        query =query.filter(models.OrderItem.price <= filters.max_price)

    sort_column = getattr(models.OrderItem,filters.sort_by,None)
    if sort_column is not None:
        sort_func = desc if filters.sort_order == "desc" else asc
        query = query.order_by (sort_func(sort_column))

    total =query.count()
    offset=(filters.page -1)* filters.limit
    items = query.offset(offset).limit(filters.limit).all()

    return {
        "total":total,
        "page":filters.page,
        "limit":filters.limit,
        "data": items
    }

#! Cart Item

def create_cart(db:Session,cart:schemas.CartItemCreate):
    if cart.user_id == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User ID is required and it can not be 0")
    if not db.query(m.User).filter(m.User.id == cart.user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User ID is not available")
    if cart.quantity == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Quantity must be greater than 0")
    if cart.product_id == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product must be greater than 0")
    
    if db.query(models.CartItem).filter(models.CartItem.user_id == cart.user_id,models.CartItem).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already has a cart")
    if db.query(models.Product).filter(models.Product.id == cart.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product is not available")
    if db.query(models.Product).filter(models.Product.id == cart.product_id,models.Product.quantity < cart.quantity):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product quantity is not available")

    
    
    db_item = models.CartItem(**cart.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_cart(db:Session,cart_id:int):
    a =db.query(models.CartItem).filter(models.CartItem.id == cart_id ).first()
    print(a)
    return db.query(models.CartItem).filter(models.CartItem.id == cart_id ).first()

def get_carts(db:Session,skip:int=0,limit:int=10):
    return db.query(models.CartItem).offset(skip).limit(limit).all()

def update_cart(db:Session,cart_id:int,cart:schemas.CartItemUpdate):
    db_cart =db.query(models.CartItem).filter(models.CartItem.id == cart_id).first()
    if not db_cart:
        return None
    
    if cart.quantity == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Quantity must be greater than 0")
    
    
    for var,value in vars(cart).items():
        setattr(db_cart,var,value)
        if not value is not None:
            setattr(db_cart,var,value)

    db.commit()
    db.refresh(db_cart)
    return db_cart

def delete_cart(db:Session,cart_id:int):
    cart = db.query(models.CartItem).filter(models.CartItem.id == cart_id).first()

    if cart:
        db.delete(cart)
        db.commit()

    return cart

def search_cart(db:Session,quantity:str):
    return db.query(models.CartItem).filter(models.CartItem.quantity.ilike(f"%{quantity}")).all()

def get_paginated_cart(db:Session,pqty:int=1,size:int=10):
    return db.query(models.CartItem).offser((pqty-1)* size).limit(size).all()

def get_all_cart_advanced(db:Session,filters:schemas.CartItemFilter):
    query=db.query(models.CartItem)
    if filters.search:
        search_term=f"%{filters.search}%"
        query=query.filter(models.CartItem.quantity.ilike(search_term))

    sort_column = getattr(models.CartItem,filters.sort_by,None)
    if sort_column is not None:
        sort_func = desc if filters.sort_order == "desc" else asc
        query = query.order_by (sort_func(sort_column))

    total =query.count()
    offset=(filters.page -1)* filters.limit
    cart = query.offset(offset).limit(filters.limit).all()

    return {
        "total":total,
        "page":filters.page,
        "limit":filters.limit,
        "data": cart
    }


    
