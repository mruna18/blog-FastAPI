from sqlalchemy import Column,Integer,String,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    name= Column(String,index=True)
    email = Column(String,unique=True,index=True)
    age = Column(Integer)
    # posts = relationship("Post",back_populates="owner",cascade="all ,delete")
    # User.posts = relationship("Post",back_populates="owner",cascade="all ,delete")
    


class Post(Base):
    __tablename__='posts'

    id =Column(Integer,primary_key=True)
    title =Column(String)
    content =Column(String)
    ower_id = Column(Integer,ForeignKey("user.id"))
    # owner =relationship("User",back_populates="posts")
    # User.posts = relationship("Post",back_populates="owner",cascade="all ,delete")
    


