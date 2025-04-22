from fastapi import APIRouter,Depends ,HTTPException
from sqlalchemy.orm import Session
from app.order import schemas,services
from app.order.dependencies import get_db


order_router =APIRouter(prefix="/order",tags=['Order'])

#! Order
@order_router.post('/createorder', response_model=schemas.OrderOut)
def create_order(order:schemas.OrderCreate,db:Session=Depends(get_db)):
    return services.create_order(db,order)

@order_router.get('/all_order',response_model =list[schemas.OrderOut])
def read_orders(skip:int=0,limit:int=10,db:Session=Depends(get_db)):
    return services.get_orders(db,skip,limit)

@order_router.get('/{order_id}',response_model =schemas.OrderOut)
def read_order(order_id:int,db:Session=Depends(get_db)):
    order = services.get_order(db,order_id)
    if not order:
        raise HTTPException(status_code=404,detail="Order not found")
    return order

@order_router.delete('/edit/{order_id}',response_model=schemas.OrderOut)
def delete_order(order_id:int,db:Session=Depends(get_db)):
    return services.delete_order(db,order_id)

#! product

@order_router.post('/products',response_model=schemas.ProductOut)
def create_products(product:schemas.ProductCreate,db:Session=Depends(get_db)):
    return services.create_product(db,product)

@order_router.get('/all_products/',response_model=list[schemas.ProductOut])
def read_products(skip:int=0,limit:int=10,db:Session=Depends(get_db)):
    return services.get_products(db,skip,limit)

@order_router.get('/get/{product_id}',response_model=schemas.ProductOut)
def read_product(product_id:int,db:Session=Depends(get_db)):
    product = services.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@order_router.put('/product/edit/{product_id}',response_model=schemas.ProductOut)
def update_product(product_id:int,product:schemas.ProductUpdate,db:Session=Depends(get_db)):
    return services.update_product(db,product_id,product)

@order_router.delete("/product/delete/{product_id}",response_model=schemas.ProductOut)
def delete_product(product_id:int,db:Session=Depends(get_db)):
    return services.delete_product(db,product_id)


@order_router.get("/product/all_product")
def get_all_products(search:str=None,min_price:int=None,max_price:int=None,sort_by:str="id",sort_order:str="asc",page:int=1,limit:int=10,db:Session=Depends(get_db),):
    filters =schemas.ProductFilter(
        search = search,min_price=min_price,max_price=max_price,sort_by =sort_by,sort_order=sort_order,page=page,limit=limit
    )
  
    return services.get_all_products_advanced(db,filters)


#! cart

@order_router.post('/cart',response_model=schemas.CartItemOut)
def create_cart(cart:schemas.CartItemCreate,db:Session= Depends(get_db)):
    return services.create_cart(db,cart)

@order_router.get('/cart/get_cart/',response_model=list[schemas.CartItemOut])
def read_carts(skip:int=0,limit:int=10,db:Session=Depends(get_db)):
    return services.get_carts(db,skip,limit)
    

@order_router.get('/cart/{cart_id}',response_model=schemas.CartItemOut)
def read_cart(cart_id:int,db:Session=Depends(get_db)):
    cart=services.get_cart(db,cart_id)
    
    if not cart:
        raise HTTPException(status_code=404,detail='Cart Item not found')
    return cart

@order_router.put('/cart/edit/{cart_id}',response_model=schemas.CartItemOut)
def update_cart(cart_id:int,user:schemas.CartItemUpdate,db:Session=Depends(get_db)):
    return services.update_cart(db,cart_id,user)

@order_router.delete("/cart/delete/{cart_id}",response_model=schemas.CartItemOut)
def delete_cart(cart_id:int,db:Session=Depends(get_db)):
    return services.delete_cart(db,cart_id)


@order_router.get("/cart/all_cart/")
def get_all_carts(search:str=None,sort_by:str="id",sort_order:str="asc",page:int=1,limit:int=10,db:Session=Depends(get_db),):
    filters =schemas.CartItemFilter(
        search = search,sort_by =sort_by,sort_order=sort_order,page=page,limit=limit
    )
    return services.get_all_cart_advanced(db,filters)


#! OrderItem
@order_router.post('/orderitem/create_orderItem',response_model=schemas.OrderItemOut)
def create_item(item:schemas.OrderItemCreate,db:Session= Depends(get_db)):
    return services.create_orderItem(db,item)

@order_router.get('/orderitem/',response_model=list[schemas.OrderItemOut])
def read_items(skip:int=0,limit:int=10,db:Session=Depends(get_db)):
    return services.get_orderItems(db,skip,limit)
    

@order_router.get('/orderitem/{orderitem_id}',response_model=schemas.OrderItemOut)
def read_item(orderitem_id:int,db:Session=Depends(get_db)):
    item=services.get_orderItem(db,orderitem_id)
    if not item:
        raise HTTPException(status_code=404,detail='order item not found')
    return item

@order_router.put('/orderitem/update/{orderitem_id}',response_model=schemas.OrderItemOut)
def update_item(orderitem_id:int,item:schemas.OrderItemUpdate,db:Session=Depends(get_db)):
    return services.update_orderItems(db,orderitem_id,item)

@order_router.delete("/orderitem/delete/{orderitem_id}",response_model=schemas.OrderItemOut)
def delete_orderitem(orderitem_id:int,db:Session=Depends(get_db)):
    return services.delete_item(db,orderitem_id)


@order_router.get("/orderitem/all_item/")
def all_orderitems(search:str=None,min_price:int=None,max_price:int=None,sort_by:str="id",sort_order:str="asc",page:int=1,limit:int=10,db:Session=Depends(get_db),):
    filters =schemas.OrderItemFilter(
        search = search,min_price=min_price,max_price=max_price,sort_by =sort_by,sort_order=sort_order,page=page,limit=limit
    )
    return services.get_all_items_advanced(db,filters)


    