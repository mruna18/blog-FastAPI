from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base



class CategoryModel(Base):
    __tablename__ = 'categories'
    c_id = Column(Integer, primary_key=True, index=True)
    cname = Column(String, nullable=False)
    soft_delete = Column(Boolean, default=False)
    p_id = Column(Integer, ForeignKey('categories.c_id'))

    parent = relationship("CategoryModel", remote_side=[c_id], backref="children")
    blogs = relationship("BlogModel", back_populates="category")


