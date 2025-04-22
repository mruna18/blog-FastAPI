from sqlalchemy import Column,Integer,String,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    price = Column(Integer)



class CartItem(Base):
    __tablename__ = 'cartitem'

    id =Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='orders')
    product_id=Column(Integer,ForeignKey('product.id'))
    product = relationship('Product', backref='orders')
    quantity = Column(Integer)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='order')
    total_amount = Column(Integer)
    
    
class OrderItem(Base):
    __tablename__ = 'orderItem'
    id = Column(Integer,primary_key=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    order = relationship('Order', backref='orderItems')
    product_id = Column(Integer,ForeignKey('product.id'))
    product = relationship('Product', backref='orderItems')
    quantity = Column(Integer)
    price=Column(Integer)

